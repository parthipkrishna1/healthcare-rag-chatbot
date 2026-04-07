import os
import xml.etree.ElementTree as ET
from langchain_core.documents import Document


def load_medquad(folder_path):

    documents = []

    for root_dir, dirs, files in os.walk(folder_path):

        for file in files:

            if file.endswith(".xml"):

                file_path = os.path.join(root_dir, file)

                tree = ET.parse(file_path)
                root = tree.getroot()

                focus_element = root.find("Focus")
                focus = focus_element.text if focus_element is not None else "Unknown"

                qa_pairs = root.find("QAPairs")

                if qa_pairs is None:
                    continue

                for qa in qa_pairs.findall("QAPair"):

                    q = qa.find("Question")
                    a = qa.find("Answer")

                    if q is None or a is None:
                        continue

                    question = q.text
                    answer = a.text

                    content = f"""
Disease: {focus}

Question: {question}

Answer:
{answer}
"""

                    documents.append(
                        Document(
                            page_content=content.strip(),
                            metadata={
                                "source": file,
                                "disease": focus
                            }
                        )
                    )

    return documents