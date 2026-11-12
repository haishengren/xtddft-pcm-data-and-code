"""Read the CSV tables in the repository's data directory."""
from pathlib import Path
import csv

DATA = Path(__file__).resolve().parents[1] / 'data'

def read_table(filename):
    """Return rows with numerical columns converted to Python numbers."""
    with (DATA / filename).open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for key, value in row.items():
            if value == '':
                row[key] = None
                continue
            try:
                row[key] = int(value)
            except ValueError:
                try:
                    row[key] = float(value)
                except ValueError:
                    pass
    return rows

def read_states(filename):
    """Use E internally for the excitation energy stored in E_eV."""
    rows = read_table(filename)
    for row in rows:
        if 'E_eV' in row:
            row['E'] = row.pop('E_eV')
    return rows
