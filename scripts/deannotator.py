# A script for creating the keystracts directory, which is a raw, unannotated collection of the keywords and abstracts
# from the downloaded ETD metadata, which has been stripped of punctuation and lowercased as a preprocessing measure.

from scripts.data_to_excel import get_etd_data
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def write_keystracts():
    logging.info("collecting metadata...")
    metadata = get_etd_data()
    file_names = [j[0] for j in metadata]
    keystracts = [re.sub('[^A-z0-9\-\s\']', '', ' '.join(k[3:])).lower() for k in metadata]
    logging.info("writing keystract files...")
    for i, fn in enumerate(file_names):
        with open("../resources/keystracts/{}.txt".format(fn), 'w', encoding='utf-8') as ks_file:
            ks_file.write(keystracts[i])
        if i % 1000 == 0 and i > 0:
            # provide file-writing update in log
            logging.info("{} keystracts written...".format(str(i)))
    logging.info("task finished; {} documents written in total.".format(str(len(metadata))))


if __name__ == "__main__":
    write_keystracts()
