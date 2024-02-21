import unittest
from unittest.mock import Mock
from dags.parse_text_store_biggquery import parse_text_files_and_store_in_bigquery
from google.cloud import storage
from google.cloud import bigquery


class TestParseAndStoreTask(unittest.TestCase):
    def test_parse_and_store_task(self):
        mock_gcs_client = Mock(spec=storage.Client())
        mock_bq_client = Mock(spec=bigquery.Client())

        parse_text_files_and_store_in_bigquery.gcs_client = mock_gcs_client
        parse_text_files_and_store_in_bigquery.bq_client = mock_bq_client

        parse_text_files_and_store_in_bigquery()

        mock_gcs_client.get_bucket.assert_called_once_with('my-gcs-bucket')
        mock_bq_client.insert_rows.assert_called_once()

        expected_parsed_data = ['192.168.1.1', '10.0.0.1', '172.16.0.1']
        self.assertEqual(
            parse_text_files_and_store_in_bigquery.parsed_data, expected_parsed_data)


if __name__ == '__main__':
    unittest.main()
