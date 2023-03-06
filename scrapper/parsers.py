import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from scrapper.types import AtomJobDict


def clean_summary_text(text: str) -> str:
    return text.removeprefix(":").strip()


def parse_job_list_atom_feed(atom_url: str) -> list[AtomJobDict]:
    response = requests.get(atom_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, features="xml")

    jobs_tags: list[Tag] = soup.find_all("entry")

    job_dict_list: list[AtomJobDict] = []
    for job in jobs_tags:
        job_dict: AtomJobDict = {}  # type: ignore[typeddict-item]

        job_url_tag = job.find("id")
        job_url = job_url_tag.text
        job_dict["job_url"] = job_url

        title_tag = job.find("title")
        title = title_tag.text.removesuffix(" - Upwork")
        job_dict["title"] = title

        summary_tag = job.find("summary")
        summary_soup = BeautifulSoup(summary_tag.text, features="lxml")

        summary_content_tag = summary_soup.find("p")
        description = summary_content_tag.next_element.text
        job_dict["description"] = description

        budget_tag = summary_soup.find("b", string="Budget")
        if budget_tag:
            budget = int(
                clean_summary_text(budget_tag.next_sibling.text)
                .removeprefix("$")
                .strip()
            )
            job_dict["budget"] = budget

        post_date_tag = summary_soup.find("b", string="Posted On")
        post_date = clean_summary_text(post_date_tag.next_sibling.text)
        job_dict["post_date"] = post_date

        category_tag = summary_soup.find("b", string="Category")
        category = clean_summary_text(category_tag.next_sibling.text)
        job_dict["category"] = category

        skills_tag = summary_soup.find("b", string="Skills")
        skills = [
            skill.strip()
            for skill in clean_summary_text(
                skills_tag.next_sibling.text,
            ).split(",")
        ]
        job_dict["skills"] = skills

        country_tag = summary_soup.find("b", string="Country")
        country = clean_summary_text(country_tag.next_sibling.text)
        job_dict["country"] = country

        job_dict_list.append(job_dict)

    return job_dict_list


if __name__ == "__main__":
    url = input("Enter Atom search url")
    jobs = parse_job_list_atom_feed(url)
    print(jobs)
