import logging
from collections import defaultdict
from http.cookiejar import MozillaCookieJar
from pathlib import Path
from typing import Union

import markdownify
import requests
import yt_dlp
from bs4 import BeautifulSoup

from kodekloud_downloader.helpers import (
    download_all_pdf,
    download_video,
    get_video_info,
    is_normal_content,
    normalize_name,
)
from kodekloud_downloader.models import Quiz, Topic

logger = logging.getLogger(__name__)


def download_quiz(output_dir: str, sep: bool):
    quiz_markdown = [] if sep else ["# KodeKloud Quiz"]
    response = requests.get("https://mcq-backend-main.kodekloud.com/api/quizzes/all")
    response.raise_for_status()

    quizzes = [Quiz(**item) for item in response.json()]
    print(f"Total {len(quizzes)} quiz available!")
    for quiz_index, quiz in enumerate(quizzes, start=1):
        quiz_name = quiz.name or quiz.topic
        quiz_markdown.append(f"\n## {quiz_name}")
        print(f"Fetching Quiz {quiz_index} - {quiz_name}")
        questions = quiz.fetch_questions()

        for index, question in enumerate(questions, start=1):
            quiz_markdown.append(f"\n**{index}. {question.question.strip()}**")
            quiz_markdown.append("\n")
            for answer in question.answers:
                quiz_markdown.append(f"* [ ] {answer}")
            quiz_markdown.append(f"\n**Correct answer:**")
            for answer in question.correctAnswers:
                quiz_markdown.append(f"* [x] {answer}")

            if script := question.code.get("script"):
                quiz_markdown.append(f"\n**Code**: \n{script}")
            if question.explanation:
                quiz_markdown.append(f"\n**Explaination**: {question.explanation}")
            if question.documentationLink:
                quiz_markdown.append(
                    f"\n**Documentation Link**: {question.documentationLink}"
                )

        if sep and quiz_name:
            output_file = Path(output_dir) / f"{quiz_name.replace('/', '')}.md"
            markdown_text = "\n".join(quiz_markdown)

            Path(output_file).write_text(markdown_text)
            print(f"Quiz file written in {output_file}")

            quiz_markdown = []
        else:
            quiz_markdown.append("\n---\n")

    if not sep:
        output_file = Path(output_dir) / "KodeKloud_Quiz.md"
        markdown_text = "\n".join(quiz_markdown)

        Path(output_file).write_text(markdown_text)
        print(f"Quiz file written in {output_file}")


def download_course(
    url: str,
    cookie: str,
    quality: str,
    output_dir: Union[str, Path],
    max_duplicate_count: int,
) -> None:
    """
    Download a course from KodeKloud.

    :param url: The course URL
    :param cookie: The user's authentication cookie
    :param quality: The video quality (e.g. "720p")
    :param output_dir: The output directory for the downloaded course
    :param max_duplicate_count: Maximum duplicate video before after cookie expire message will be raised
    """
    cj = MozillaCookieJar(cookie)
    cj.load(ignore_discard=True, ignore_expires=True)

    page = requests.get(url, cookies=cj)
    soup = BeautifulSoup(page.content, "html.parser")
    course_name_tag = soup.find("h1", class_="course_title") or soup.find(
        "h1", class_="entry-title"
    )
    course_name = course_name_tag.text.strip()
    main_lesson_content = soup.find("div", class_="lessons_main__content") or soup.find(
        "div", class_="ld-lesson-list"
    )
    topics = (
        main_lesson_content.find_all("div", class_="ld-item-list-item")
        or main_lesson_content.find_all("div", class_="w-dyn-item")
        or main_lesson_content.find_all("div", class_="ld-item-list-items")
    )
    items = [Topic.make(topic) for topic in topics]

    downloaded_videos = defaultdict(int)
    for i, item in enumerate(items, start=1):
        for j, lesson in enumerate(item.lessons, start=1):
            file_path = create_file_path(
                output_dir, course_name, i, item.name, j, lesson.name
            )

            if lesson.is_video:
                current_video_url = get_video_info(lesson.url, cookie=cookie).get("url")
                if (
                    current_video_url in downloaded_videos
                    and downloaded_videos[current_video_url] > max_duplicate_count
                ):
                    raise SystemExit(
                        f"The folowing video is downloaded more than {max_duplicate_count}."
                        "\nYour cookie might have expired or you don't have access/enrolled to the course."
                        "\nPlease refresh/regenerate the cookie or enroll in the course and try again."
                    )
                download_video_lesson(lesson, file_path, cookie, quality)
                downloaded_videos[current_video_url] += 1
            else:
                download_resource_lesson(lesson, file_path, cookie)


def create_file_path(
    output_dir: Union[str, Path],
    course_name: str,
    i: int,
    item_name: str,
    j: int,
    lesson_name: str,
) -> Path:
    """
    Create a file path for a lesson.

    :param output_dir: The output directory for the downloaded course
    :param course_name: The course name
    :param i: The topic index
    :param item_name: The topic name
    :param j: The lesson index
    :param lesson_name: The lesson name
    :return: The created file path
    """
    return Path(
        Path(output_dir)
        / "KodeKloud"
        / normalize_name(course_name)
        / f"{i} - {normalize_name(item_name)}"
        / f"{j} - {normalize_name(lesson_name)}"
    )


def download_video_lesson(lesson, file_path: Path, cookie: str, quality: str) -> None:
    """
    Download a video lesson.

    :param lesson: The lesson object
    :param file_path: The output file path for the video
    :param cookie: The user's authentication cookie
    :param quality: The video quality (e.g. "720p")
    """
    logger.info(f"Writing video file... {file_path}...")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Parsing url: {lesson.url}")
    try:
        download_video(
            url=lesson.url,
            output_path=file_path,
            cookie=cookie,
            quality=quality,
        )
    except yt_dlp.utils.UnsupportedError as ex:
        logger.error(
            f"Could not download video in link {lesson.url}. "
            "Please open link manually and verify that video exists!"
        )
    except yt_dlp.utils.DownloadError as ex:
        logger.error(
            f"Access denied while downloading video or audio file from link {lesson.url}"
        )


def download_resource_lesson(lesson, file_path: Path, cookie: str) -> None:
    """
    Download a resource lesson.

    :param lesson: The lesson object
    :param file_path: The output file path for the resource
    :param cookie: The user's authentication cookie
    """
    page = requests.get(lesson.url)
    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find("div", class_="learndash_content_wrap")

    if content and is_normal_content(content):
        logger.info(f"Writing resource file... {file_path}...")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.with_suffix(".md").write_text(
            markdownify.markdownify(content.prettify()), encoding="utf-8"
        )
        download_all_pdf(content=content, download_path=file_path.parent, cookie=cookie)
