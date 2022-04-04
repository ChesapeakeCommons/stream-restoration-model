#!/usr/bin/env python

from app import db


class LoadRates(db.Model):

    __tablename__ = 'load_rates'

    __table_args__ = {
        'extend_existing': True,
    }

    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.Text)

    source = db.Column(db.Text)

    normalized_source = db.Column(db.Text)

    load_rate = db.Column(db.Numeric)

    n = db.Column(db.Numeric)

    p = db.Column(db.Numeric)

    tss = db.Column(db.Numeric)
