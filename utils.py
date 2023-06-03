from datetime import datetime as datetime


def adjust_types(data):
    data = data.astype(
        {
            "Date": str,
            "Open": float,
            "High": float,
            "Low": float,
            "Close": float,
            "Volume": float,
            "ITVS": float,
            "Signal": float,
            "P/L": float,
            "Capital": float,
        }
    )
    return data
