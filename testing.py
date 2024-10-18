from sqlite3 import Error
from unittest.mock import MagicMock, patch
from unittest.mock import MagicMock, patch
import pytest





from data_extractor.file_loaders.docx_loader import DOCXLoader
from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.file_loaders.ppt_loader import PPTLoader
from data_extractor.storage.sql_storage import SQLStorage
from data_extractor.data_extractor.docx_extractor import DOCXExtractor
from data_extractor.data_extractor.pptx_extractor import PPTXExtractor

@pytest.fixture
def docx_loader():
    return DOCXLoader()





def test_validate_file_no_extension(docx_loader):
    no_extension_path = "test_files/docx/no_extension"
    with pytest.raises(ValueError, match="Invalid DOCX file."):
        docx_loader.load_file(no_extension_path)





def test_validate_uppercase_docx_extension(docx_loader):
    uppercase_docx_path = "test_files/docx/UPPERCASE.DOCX"
    assert docx_loader.validate_file(uppercase_docx_path), "Failed to validate .DOCX with uppercase extension"


def test_validate_mixed_case_docx_extension(docx_loader):
    mixed_case_docx_path = "test_files/docx/mixedCase.DoCx"
    assert docx_loader.validate_file(mixed_case_docx_path), "Failed to validate .DoCx file"


def test_validate_file_with_spaces(docx_loader):
    file_with_spaces_path = "test_files/docx/file with spaces.docx"
    assert docx_loader.validate_file(file_with_spaces_path), "Failed to validate .docx file with spaces in the name"


def test_validate_file_with_special_characters(docx_loader):
    special_characters_path = "test_files/docx/special_#@!.docx"
    assert docx_loader.validate_file(special_characters_path), "Failed to validate .docx file with special characters"


def test_validate_empty_string_path(docx_loader):
    empty_string_path = ""
    with pytest.raises(ValueError, match="Invalid DOCX file."):
        docx_loader.load_file(empty_string_path)


def test_validate_file_with_long_name(docx_loader):
    long_name_path = "test_files/docx/" + "a" * 255 + ".docx"
    assert docx_loader.validate_file(long_name_path), "Failed to validate .docx file with a long name"


def test_validate_file_with_multiple_dots(docx_loader):
    multiple_dots_path = "test_files/docx/multiple.dots.file.docx"
    assert docx_loader.validate_file(multiple_dots_path), "Failed to validate .docx file with multiple dots in the name"


def test_validate_invalid_docx_extension(docx_loader):
    invalid_extension_path = "test_files/docx/invalid.docxx"
    with pytest.raises(ValueError, match="Invalid DOCX file."):
        docx_loader.load_file(invalid_extension_path)



def test_validate_incorrect_extension_valid_content(docx_loader):
    incorrect_extension_path = "test_files/docx/valid_content_wrong_extension.pdf"
    with pytest.raises(ValueError, match="Invalid DOCX file."):
        docx_loader.load_file(incorrect_extension_path)




def test_validate_deeply_nested_file(docx_loader):
    deeply_nested_path = "test_files/docx/nested_folder/subfolder/deepfile.docx"
    assert docx_loader.validate_file(deeply_nested_path), "Failed to validate .docx file in a deeply nested folder"






@pytest.fixture
def pdf_loader():
    return PDFLoader()


def test_validate_valid_pdf_file(pdf_loader):
    valid_pdf_path = "test_files/pdf/valid_file.pdf"
    assert pdf_loader.validate_file(valid_pdf_path), "Failed to validate a valid PDF file."


def test_validate_pdf_file_with_spaces(pdf_loader):
    pdf_with_spaces_path = "test_files/pdf/file with spaces.pdf"
    assert pdf_loader.validate_file(pdf_with_spaces_path), "Failed to validate PDF file with spaces in the name."



def test_validate_empty_string_path(pdf_loader):
    empty_string_path = ""
    with pytest.raises(ValueError, match="Invalid PDF file."):
        pdf_loader.load_file(empty_string_path)


def test_validate_pdf_file_with_long_name(pdf_loader):
    long_name_path = "test_files/pdf/" + "a" * 255 + ".pdf"
    assert pdf_loader.validate_file(long_name_path), "Failed to validate PDF file with a long name."




def test_validate_pdf_file_with_multiple_dots(pdf_loader):
    multiple_dots_path = "test_files/pdf/multiple.dots.file.pdf"
    assert pdf_loader.validate_file(multiple_dots_path), "Failed to validate PDF file with multiple dots in the name."



def test_validate_hidden_pdf_file(pdf_loader):
    hidden_file_path = "test_files/pdf/.hidden_file.pdf"
    assert pdf_loader.validate_file(hidden_file_path), "Failed to validate hidden PDF file."



def test_validate_invalid_pdf_extension(pdf_loader):
    invalid_extension_path = "test_files/pdf/invalid.pdfx"
    with pytest.raises(ValueError, match="Invalid PDF file."):
        pdf_loader.load_file(invalid_extension_path)



def test_validate_incorrect_extension_valid_content(pdf_loader):
    incorrect_extension_path = "test_files/pdf/valid_content_wrong_extension.txt"
    with pytest.raises(ValueError, match="Invalid PDF file."):
        pdf_loader.load_file(incorrect_extension_path)



@pytest.fixture
def ppt_loader():
    return PPTLoader()




def test_validate_valid_pptx_file(ppt_loader):
    valid_pptx_path = "test_files/ppt/valid_file.pptx"
    assert ppt_loader.validate_file(valid_pptx_path), "Failed to validate a valid PPTX file."



def test_validate_valid_ppt_file(ppt_loader):
    valid_ppt_path = "test_files/ppt/valid_file.ppt"
    assert ppt_loader.validate_file(valid_ppt_path), "Failed to validate a valid PPT file."


def test_validate_ppt_file_with_spaces(ppt_loader):
    ppt_with_spaces_path = "test_files/ppt/file with spaces.pptx"
    assert ppt_loader.validate_file(ppt_with_spaces_path), "Failed to validate PPTX file with spaces in the name."


def test_validate_ppt_file_with_special_characters(ppt_loader):
    special_characters_path = "test_files/ppt/special_#@!.pptx"
    assert ppt_loader.validate_file(special_characters_path), "Failed to validate PPTX file with special characters."


def test_validate_empty_string_path(ppt_loader):
    empty_string_path = ""
    with pytest.raises(ValueError, match="Invalid PPT file."):
        ppt_loader.load_file(empty_string_path)

def test_validate_ppt_file_with_long_name(ppt_loader):
    long_name_path = "test_files/ppt/" + "a" * 255 + ".pptx"
    assert ppt_loader.validate_file(long_name_path), "Failed to validate PPTX file with a long name."

def test_validate_ppt_file_with_multiple_dots(ppt_loader):
    multiple_dots_path = "test_files/ppt/multiple.dots.file.pptx"
    assert ppt_loader.validate_file(multiple_dots_path), "Failed to validate PPTX file with multiple dots in the name."



def test_validate_hidden_ppt_file(ppt_loader):
    hidden_file_path = "test_files/ppt/.hidden_file.pptx"
    assert ppt_loader.validate_file(hidden_file_path), "Failed to validate hidden PPTX file."


def test_validate_invalid_ppt_extension(ppt_loader):
    invalid_extension_path = "test_files/ppt/invalid.pptx_invalid"
    with pytest.raises(ValueError, match="Invalid PPT file."):
        ppt_loader.load_file(invalid_extension_path)




@pytest.fixture
def ppt_loader():
    return PPTLoader()

@pytest.fixture
def pptx_extractor(ppt_loader):
    return PPTXExtractor(ppt_loader)

def test_load_valid_pptx(pptx_extractor):
    file_path = "test_files/pptx/empty.pptx"  # Adjust path to a valid PPTX file
    pptx_extractor.load(file_path)
    assert pptx_extractor.file is not None, "Failed to load PPTX file."


@pytest.fixture
def mock_loader():
    """Mock the PPTLoader."""
    return MagicMock()

@pytest.fixture
def pptx_extractor(mock_loader):
    """Create a PPTXExtractor with the mocked loader."""
    return PPTXExtractor(mock_loader)


def test_load_valid_pptx(pptx_extractor, mock_loader):
    """Test loading a valid PPTX file."""
    mock_loader.load_file.return_value = MagicMock()  # Mock a presentation object
    pptx_extractor.load("fake_path.pptx")

def test_load_valid_pptx(pptx_extractor, mock_loader):
    """Test loading a valid PPTX file."""
    mock_loader.load_file.return_value = MagicMock()  # Mock a presentation object
    pptx_extractor.load("fake_path.pptx")
    
    assert pptx_extractor.file is not None, "Failed to load PPTX file."

def test_extract_text(pptx_extractor, mock_loader):
    """Test text extraction from PPTX."""
    # Mock the loaded PPTX with slides and shapes
    mock_slide = MagicMock()
    mock_shape = MagicMock()
    mock_shape.text = "Sample text"
    mock_slide.shapes = [mock_shape]
    mock_loader.load_file.return_value.slides = [mock_slide]

    pptx_extractor.load("fake_path.pptx")
    text = pptx_extractor.extract_text()
    
    assert text == "Sample text\n", "Text extraction did not return expected result."






def test_extract_images(pptx_extractor, mock_loader):
    """Test image extraction from PPTX."""
    # Mock the loaded PPTX with images
    mock_slide = MagicMock()
    mock_shape = MagicMock()
    mock_shape.shape_type = 13  # Indicates a picture shape
    mock_shape.image.blob = b'image_data'
    mock_shape.image.ext = 'png'
    mock_slide.shapes = [mock_shape]
    mock_loader.load_file.return_value.slides = [mock_slide]

    pptx_extractor.load("fake_path.pptx")
    images = pptx_extractor.extract_images()
    
    assert len(images) == 1, "No images extracted from PPTX file."
    assert images[0]["image_data"] == b'image_data', "Extracted image data does not match."
    assert images[0]["ext"] == 'png', "Extracted image extension does not match."

def test_extract_urls(pptx_extractor, mock_loader):
    """Test URL extraction from PPTX."""
    # Mock the loaded PPTX with links
    mock_slide = MagicMock()
    mock_shape = MagicMock()
    mock_paragraph = MagicMock()
    mock_run = MagicMock()
    mock_run.text = "Click here"
    mock_run.hyperlink.address = "http://example.com"
    mock_paragraph.runs = [mock_run]
    mock_shape.text_frame = MagicMock()
    mock_shape.text_frame.paragraphs = [mock_paragraph]
    mock_slide.shapes = [mock_shape]
    mock_loader.load_file.return_value.slides = [mock_slide]

    pptx_extractor.load("fake_path.pptx")
    urls = pptx_extractor.extract_urls()

    assert len(urls) == 1, "No URLs extracted from PPTX file."
    assert urls[0]["linked_text"] == "Click here", "Linked text does not match."
    assert urls[0]["url"] == "http://example.com", "URL does not match."
    assert urls[0]["page_number"] == 1, "Page number does not match."

def test_extract_tables(pptx_extractor, mock_loader):
    """Test table extraction from PPTX."""
    # Mock the loaded PPTX with tables
    mock_slide = MagicMock()
    mock_shape = MagicMock()
    mock_shape.has_table = True
    mock_shape.table.rows = [
        MagicMock(cells=[MagicMock(text_frame=MagicMock(text='Cell 1')), 
                         MagicMock(text_frame=MagicMock(text='Cell 2'))]),
        MagicMock(cells=[MagicMock(text_frame=MagicMock(text='Cell 3')), 
                         MagicMock(text_frame=MagicMock(text='Cell 4'))])
    ]
    mock_slide.shapes = [mock_shape]
    mock_loader.load_file.return_value.slides = [mock_slide]

    pptx_extractor.load("fake_path.pptx")
    tables = pptx_extractor.extract_tables()

    assert len(tables) == 1, "No tables extracted from PPTX file."
    assert tables[0] == [['Cell 1', 'Cell 2'], ['Cell 3', 'Cell 4']], "Table content does not match."






# for sql storage test


@pytest.fixture
def mock_connection():
    """Create a mock SQLite connection."""
    return MagicMock()



@pytest.fixture
def sql_storage(mock_connection):
    """Create an instance of SQLStorage with a mocked connection."""
    with patch('sqlite3.connect', return_value=mock_connection):
        storage = SQLStorage(connection_string="mock_connection_string")
        yield storage




def test_store_inserts_data(sql_storage, mock_connection):
    """Test if the store method inserts data into the table."""
    sql_storage.store("TestTable", {"key": "value"})

    # Verify that the data was inserted into the table
    escaped_table_name = '"TestTable"'
    mock_connection.cursor().execute.assert_any_call(
        f"INSERT INTO {escaped_table_name} (data) VALUES (?)", (str({"key": "value"}),)
    )


def test_close_connection(sql_storage, mock_connection):
    """Test if the close method closes the database connection."""
    sql_storage.close()
    mock_connection.close.assert_called_once()



def test_store_creates_table_with_escaped_name(sql_storage, mock_connection):
    """Test if the store method creates a table with an escaped name."""
    sql_storage.store("Table Name With Space", {"key": "value"})

    # Check if the table was created with the correct escaped name
    escaped_table_name = '"Table_Name_With_Space"'
    
    # Assert that the CREATE TABLE statement was called
    mock_connection.cursor().execute.assert_any_call(
        f"""CREATE TABLE IF NOT EXISTS {escaped_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )"""
    )    



def test_store_inserts_data(sql_storage, mock_connection):
    """Test if the store method inserts data into the table."""
    sql_storage.store("TestTable", {"key": "value"})

    # Verify that the data was inserted into the table
    escaped_table_name = '"TestTable"'
    mock_connection.cursor().execute.assert_any_call(
        f"INSERT INTO {escaped_table_name} (data) VALUES (?)", (str({"key": "value"}),)
    )   



def test_close_connection(sql_storage, mock_connection):
    """Test if the close method closes the database connection."""
    sql_storage.close()
    mock_connection.close.assert_called_once()     







def test_store_inserts_empty_data(sql_storage, mock_connection):
    """Test if the store method can handle empty data."""
    sql_storage.store("EmptyTable", {})
    
    # Verify that the data was inserted into the table
    escaped_table_name = '"EmptyTable"'
    mock_connection.cursor().execute.assert_any_call(
        f"INSERT INTO {escaped_table_name} (data) VALUES (?)", (str({}),)
    )


def test_store_creates_table_with_special_characters(sql_storage, mock_connection):
    """Test if the store method creates a table with special characters in the name."""
    sql_storage.store("Table#With$Special%Characters", {"key": "value"})
    
    # Check if the table was created with the correct escaped name
    escaped_table_name = '"Table#With$Special%Characters"'
    mock_connection.cursor().execute.assert_any_call(
        f"""CREATE TABLE IF NOT EXISTS {escaped_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )"""
    )




def test_close_connection_is_called_after_operations(sql_storage, mock_connection):
    """Test if the close method is called after storing data."""
    sql_storage.store("CloseTestTable", {"key": "value"})
    sql_storage.close()
    
    # Assert that the close method was called
    mock_connection.close.assert_called_once()


def test_store_with_table_name_in_lowercase(sql_storage, mock_connection):
    """Test if the store method handles lowercase table names correctly."""
    sql_storage.store("lowercase_table", {"key": "value"})

    # Check if the table was created with the correct escaped name
    escaped_table_name = '"lowercase_table"'
    mock_connection.cursor().execute.assert_any_call(
        f"""CREATE TABLE IF NOT EXISTS {escaped_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )"""
    )


def test_store_inserts_large_data(sql_storage, mock_connection):
    """Test if the store method can handle large data."""
    large_data = "x" * 10000  # 10,000 characters
    sql_storage.store("LargeDataTable", {"large_key": large_data})

    escaped_table_name = '"LargeDataTable"'
    mock_connection.cursor().execute.assert_any_call(
        f"INSERT INTO {escaped_table_name} (data) VALUES (?)", (str({"large_key": large_data}),)
    )













# def test_validate_small_docx_file(docx_loader):
#     small_docx_path = "test_files/docx/small.docx"
#     assert docx_loader.load_file(small_docx_path), f"Loaded DOCX file: {small_docx_path}"

# def test_validate_large_docx_file(docx_loader):
#     large_docx_path = "test_files/docx/large.docx"
#     assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

# def test_validate_corrupted_docx_file(docx_loader):
#     corrupted_docx_path = "test_files/docx/corrupted.docx"
#     with pytest.raises(ValueError, match="Invalid DOCX file."):
#         docx_loader.load_file(corrupted_docx_path)

# def test_validate_non_docx_file(docx_loader):
#     non_docx_path = "test_files/pdf/small.pdf"
#     with pytest.raises(ValueError, match="Invalid DOCX file."):
#         docx_loader.load_file(non_docx_path)

# def test_validate_empty_docx_file(docx_loader):
#     empty_docx_path = "test_files/docx/empty.docx"
#     assert docx_loader.load_file(empty_docx_path), f"Loaded DOCX file: {empty_docx_path}"

# def test_validate_docx_with_complex_formatting(docx_loader):
#     large_docx_path = "test_files/docx/large.docx"
#     assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

# def test_validate_password_protected_docx(docx_loader):
#     protected_docx_path = "test_files/docx/password.docx"
#     with pytest.raises(ValueError, match="Invalid DOCX file."):
#         docx_loader.load_file(protected_docx_path)

# def test_validate_docx_with_embedded_links(docx_loader):
#     large_docx_path = "test_files/docx/large.docx"
#     assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

# def test_validate_docx_with_embedded_images(docx_loader):
#     large_docx_path = "test_files/docx/large.docx"
#     assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

# def test_validate_docx_with_multiple_sections(docx_loader):
#     large_docx_path = "test_files/docx/large.docx"
#     assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"

# def test_validate_docx_with_comments_or_track_changes(docx_loader):
#     large_docx_path = "test_files/docx/large.docx"
#     assert docx_loader.load_file(large_docx_path), f"Loaded DOCX file: {large_docx_path}"






# @pytest.fixture
# def pdf_loader():
#     return PDFLoader()

# def test_validate_small_pdf_file(pdf_loader):
#     small_pdf_path = "test_files/pdf/small.pdf"
#     assert pdf_loader.load_file(small_pdf_path), f"Loaded PDF file: {small_pdf_path}"

# def test_validate_large_pdf_file(pdf_loader):
#     large_pdf_path = "test_files/pdf/large.pdf"
#     assert pdf_loader.load_file(large_pdf_path), f"Loaded PDF file: {large_pdf_path}"

# def test_validate_corrupted_pdf_file(pdf_loader):
#     corrupted_pdf_path = "test_files/pdf/corrupted.pdf"
#     with pytest.raises(ValueError, match="Invalid PDF file."):
#         pdf_loader.load_file(corrupted_pdf_path)

# def test_validate_non_pdf_file(pdf_loader):
#     non_pdf_path = "test_files/docx/small.docx"
#     with pytest.raises(ValueError, match="Invalid PDF file."):
#         pdf_loader.load_file(non_pdf_path)

# def test_validate_empty_pdf_file(pdf_loader):
#     empty_pdf_path = "test_files/pdf/empty.pdf"
#     assert pdf_loader.load_file(empty_pdf_path), f"Loaded PDF file: {empty_pdf_path}"

# def test_validate_password_protected_pdf(pdf_loader):
#     protected_pdf_path = "test_files/pdf/password.pdf"
#     with pytest.raises(ValueError, match="Invalid PDF file."):
#         pdf_loader.load_file(protected_pdf_path)

# def test_validate_pdf_with_embedded_links(pdf_loader):
#     pdf_with_links_path = "test_files/pdf/large.pdf"
#     assert pdf_loader.load_file(pdf_with_links_path), f"Loaded PDF file: {pdf_with_links_path}"

# def test_validate_pdf_with_embedded_images(pdf_loader):
#     pdf_with_images_path = "test_files/pdf/large.pdf"
#     assert pdf_loader.load_file(pdf_with_images_path), f"Loaded PDF file: {pdf_with_images_path}"

# def test_validate_pdf_with_multiple_pages(pdf_loader):
#     multi_page_pdf_path = "test_files/pdf/large.pdf"
#     assert pdf_loader.load_file(multi_page_pdf_path), f"Loaded PDF file: {multi_page_pdf_path}"

# def test_validate_pdf_with_comments(pdf_loader):
#     pdf_with_comments_path = "test_files/pdf/large.pdf"
#     assert pdf_loader.load_file(pdf_with_comments_path), f"Loaded PDF file: {pdf_with_comments_path}"

# @pytest.fixture
# def ppt_loader():
#     return PPTLoader()

# def test_validate_small_pptx_file(ppt_loader):
#     small_pptx_path = "test_files/pptx/small.pptx"
#     assert ppt_loader.load_file(small_pptx_path), f"Loaded PPTX file: {small_pptx_path}"

# def test_validate_large_pptx_file(ppt_loader):
#     large_pptx_path = "test_files/pptx/large.pptx"
#     assert ppt_loader.load_file(large_pptx_path), f"Loaded PPTX file: {large_pptx_path}"

# def test_validate_corrupted_pptx_file(ppt_loader):
#     corrupted_pptx_path = "test_files/pptx/corrupted.pptx"
#     with pytest.raises(ValueError, match="Invalid PPT file."):
#         ppt_loader.load_file(corrupted_pptx_path)

# def test_validate_non_pptx_file(ppt_loader):
#     non_pptx_path = "test_files/pdf/small.pdf"
#     with pytest.raises(ValueError, match="Invalid PPT file."):
#         ppt_loader.load_file(non_pptx_path)

# def test_validate_empty_pptx_file(ppt_loader):
#     empty_pptx_path = "test_files/pptx/empty.pptx"
#     assert ppt_loader.load_file(empty_pptx_path), f"Loaded PPTX file: {empty_pptx_path}"

# def test_validate_pptx_with_complex_animations(ppt_loader):
#     complex_animations_pptx_path = "test_files/pptx/large.pptx"
#     assert ppt_loader.load_file(complex_animations_pptx_path), f"Loaded PPTX file: {complex_animations_pptx_path}"

# def test_validate_password_protected_pptx(ppt_loader):
#     protected_pptx_path = "test_files/pptx/password.pptx"
#     with pytest.raises(ValueError, match="Invalid PPT file."):
#         ppt_loader.load_file(protected_pptx_path)

# def test_validate_pptx_with_embedded_links(ppt_loader):
#     links_pptx_path = "test_files/pptx/large.pptx"
#     assert ppt_loader.load_file(links_pptx_path), f"Loaded PPTX file: {links_pptx_path}"

# def test_validate_pptx_with_embedded_images(ppt_loader):
#     images_pptx_path = "test_files/pptx/large.pptx"
#     assert ppt_loader.load_file(images_pptx_path), f"Loaded PPTX file: {images_pptx_path}"

# def test_validate_pptx_with_videos(ppt_loader):
#     video_pptx_path = "test_files/pptx/large.pptx"
#     assert ppt_loader.load_file(video_pptx_path), f"Loaded PPTX file: {video_pptx_path}"

# def test_validate_pptx_with_multiple_slides_and_transitions(ppt_loader):
#     multiple_slides_pptx_path = "test_files/pptx/large.pptx"
#     assert ppt_loader.load_file(multiple_slides_pptx_path), f"Loaded PPTX file: {multiple_slides_pptx_path}"

# def test_validate_pptx_with_embedded_audio(ppt_loader):
#     audio_pptx_path = "test_files/pptx/large.pptx"
#     assert ppt_loader.load_file(audio_pptx_path), f"Loaded PPTX file: {audio_pptx_path}"

# def test_validate_pptx_with_custom_slide_layouts(ppt_loader):
#     custom_layout_pptx_path = "test_files/pptx/large.pptx"
#     assert ppt_loader.load_file(custom_layout_pptx_path), f"Loaded PPTX file: {custom_layout_pptx_path}"
    
# @pytest.fixture
# def valid_db_path():
#     """Fixture for the valid SQLite database path."""
#     return "assignment4.db"

# @pytest.fixture
# def invalid_db_path():
#     """Fixture for an invalid SQLite database path."""
#     return "/invalid/path/to/assignment4.db"

# @pytest.fixture
# def sql_storage(valid_db_path):
#     """Fixture for SQLStorage with a valid database path."""
#     return SQLStorage(valid_db_path)

# @pytest.fixture
# def mock_cursor():
#     """Mock the cursor and connection for SQLite."""
#     cursor_mock = MagicMock()
#     connection_mock = MagicMock()
#     cursor_mock.cursor.return_value = cursor_mock
#     cursor_mock.__enter__.return_value = cursor_mock
#     connection_mock.connect.return_value = connection_mock
#     return cursor_mock, connection_mock

# def test_validate_successful_database_connection(mocker, valid_db_path):
#     # Mock the connect method from sqlite3 to return a mock connection
#     mocker.patch('sqlite3.connect', return_value=mocker.Mock())
#     storage = SQLStorage(database=valid_db_path)
#     assert storage.connection is not None, "Connected to SQLite database"

# def test_validate_failed_database_connection(mocker, invalid_db_path):
#     # Mock the connect method to raise a connection error
#     mocker.patch('sqlite3.connect', side_effect=Error("Failed to connect"))
#     with pytest.raises(SystemExit):  # Assuming your code exits on failure
#         SQLStorage(database=invalid_db_path)


# def test_retrieve_all_stored_text_data(sql_storage, mock_cursor):
#     """Test retrieving all stored text data."""
#     with patch('sqlite3.connect', return_value=mock_cursor[1]):
#         with patch.object(mock_cursor[1], 'cursor', return_value=mock_cursor[0]):
#             # Store some example text data
#             sql_storage.store("text_data", [{'page_number': 1, 'text': 'Example text'}])
            
#             # Simulate data retrieval
#             mock_cursor[0].execute.return_value = [("Example text",)]
#             data = sql_storage.retrieve_all("text_data")
            
#             # Verify that data is retrieved
#             assert data == [("Example text",)]
#             assert mock_cursor[0].execute.call_count > 0

# def test_retrieve_stored_links_data(sql_storage, mock_cursor):
#     """Test retrieving all stored hyperlinks data."""
#     with patch('sqlite3.connect', return_value=mock_cursor[1]):
#         with patch.object(mock_cursor[1], 'cursor', return_value=mock_cursor[0]):
#             # Store some example hyperlinks data
#             sql_storage.store("links_data", [{'url': 'http://example.com', 'page_number': 1}])
            
#             # Simulate data retrieval
#             mock_cursor[0].execute.return_value = [("http://example.com",)]
#             data = sql_storage.retrieve_all("links_data")
            
#             # Verify that data is retrieved
#             assert data == [("http://example.com",)]
#             assert mock_cursor[0].execute.call_count > 0

# def test_retrieve_table_metadata(sql_storage, mock_cursor):
#     """Test retrieving table metadata."""
#     with patch('sqlite3.connect', return_value=mock_cursor[1]):
#         with patch.object(mock_cursor[1], 'cursor', return_value=mock_cursor[0]):
#             # Store some table metadata
#             sql_storage.store("table_metadata", [{'page_number': 1, 'csv_filename': 'table1.csv'}])
            
#             # Simulate data retrieval
#             mock_cursor[0].execute.return_value = [("table1.csv",)]
#             data = sql_storage.retrieve_all("table_metadata")
            
#             # Verify that data is retrieved
#             assert data == [("table1.csv",)]
#             assert mock_cursor[0].execute.call_count > 0
