import re
import time
from psycopg2 import sql
from .database import normalize_text, PostgresDB

db = PostgresDB()
db.connect()

def find_snippets_in_text(source_language, target_language, text):
    if source_language not in ["fr", "de", "en"]:
        return "Invalid source language"

    if target_language not in ["fr", "de", "en"]:
        return "Invalid target language"

    snippets = db.fetch_snippets(source_language, target_language)
    normalized_text = normalize_text(text)

    replacements = []
    start_time = time.time() 

    # Sort snippets by length in descending order to prioritize longer matches
    sorted_snippets = sorted(snippets, key=lambda x: len(x[1]), reverse=True)

    for snippet_id, snippet, translation in sorted_snippets:
        normalized_snippet = normalize_text(snippet)
        if normalized_snippet in normalized_text:
            replacements.append((snippet, str(snippet_id)))

    # Perform replacements in the original text
    for snippet, snippet_id in replacements:
        text = re.sub(re.escape(snippet), snippet_id, text, flags=re.IGNORECASE)

    end_time = time.time()  # End measuring time

    # Calculate time taken for the operation
    time_taken = end_time - start_time
    print(f"Finished in: {time_taken:.4f} s")

    return text


def replace_ids_with_translations_in_raw_text(target_language, text):
    try:
        with db.connection.cursor() as cursor:
            query = sql.SQL("""
                SELECT id, {target_field}
                FROM translations
            """).format(
                target_field=sql.Identifier(target_language)
            )
            cursor.execute(query)
            translations = cursor.fetchall()

            id_to_translation = {str(id): translation for id, translation in translations}

            def replace_id(match):
                snippet_id = match.group(0)
                return id_to_translation.get(snippet_id, snippet_id)

            # Replace IDs with translations
            text = re.sub(r'\b\d+\b', replace_id, text)

            return text
    except Exception as e:
        print(f"Error replacing IDs with translations: {e}")
        return text


def replace_snippets_with_ids(doc, source_lang, target_lang):
    for para in doc.paragraphs:
        replace_snippets_in_paragraph(para, source_lang, target_lang)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    replace_snippets_in_paragraph(para, source_lang, target_lang)
    return doc

def replace_snippets_in_paragraph(paragraph, source_lang, target_lang):
    full_text = ''.join(run.text for run in paragraph.runs)
    replaced_text = find_snippets_in_text(source_lang, target_lang, full_text)

    if full_text != replaced_text:
        apply_replaced_text(paragraph, replaced_text)

def apply_replaced_text(paragraph, replaced_text):
    runs = list(paragraph.runs)
    current_pos = 0

    for run in runs:
        run_length = len(run.text)
        if current_pos < len(replaced_text):
            run.text = replaced_text[current_pos:current_pos + run_length]
        else:
            run.text = ''
        current_pos += run_length

    if current_pos < len(replaced_text):
        remaining_text = replaced_text[current_pos:]
        new_run = paragraph.add_run(remaining_text)
        new_run.font.bold = runs[-1].font.bold
        new_run.font.italic = runs[-1].font.italic
        new_run.font.underline = runs[-1].font.underline
        new_run.font.color.rgb = runs[-1].font.color.rgb
        new_run.font.size = runs[-1].font.size
        new_run.font.name = runs[-1].font.name

def replace_ids_with_translations_in_docx(doc, target_lang):
    for para in doc.paragraphs:
        replace_ids_in_paragraph(para, target_lang)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    replace_ids_in_paragraph(para, target_lang)
    return doc

def replace_ids_in_paragraph(paragraph, target_lang):
    full_text = ''.join(run.text for run in paragraph.runs)
    replaced_text = replace_ids_with_translations_in_raw_text(target_lang, full_text)

    if full_text != replaced_text:
        apply_replaced_text(paragraph, replaced_text)
