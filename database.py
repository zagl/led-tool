#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import sqlite3


class LedDatabase(object):

    def __init__(self):
        filename = "led-tool.db"
        new = not os.path.exists(filename)
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()
        if new:
            self.c.execute("""CREATE TABLE manufacturers(
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE)"""
            )

            self.c.execute("""CREATE TABLE families(
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE)"""
            )

            self.c.execute("""CREATE TABLE leds(
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                family INTEGER,
                manufacturer INTEGER,
                thermal_resistance_jb FLOAT,
                reference_temperature FLOAT,
                typical_voltage FLOAT,
                typical_current FLOAT)"""
            )

            self.c.execute("""CREATE TABLE wavelength_vs_relative_spectral_emission(
                led INTEGER,
                wavelength FLOAT,
                emission FLOAT)"""
            )

            self.c.execute("""CREATE TABLE current_vs_voltage(
                led INTEGER,
                current FLOAT,
                voltage FLOAT)"""
            )

            self.c.execute("""CREATE TABLE current_vs_relative_luminous_flux(
                led INTEGER,
                current FLOAT,
                flux FLOAT)"""
            )

            self.c.execute("""CREATE TABLE temperature_vs_relative_forward_voltage(
                led INTEGER,
                temperature FLOAT,
                voltage FLOAT)"""
            )

            self.c.execute("""CREATE TABLE temperature_vs_relative_luminous_flux(
                led INTEGER,
                temperature FLOAT,
                flux FLOAT)"""
            )

            self.conn.commit()

    def addBrand(self, name):
        self.c.execute("INSERT INTO manufacturers VALUES (NULL,?)", (name,))
        self.conn.commit()

    def addFamily(self, name):
        self.c.execute("INSERT INTO families VALUES (NULL,?)", (name,))
        self.conn.commit()

    def addLed(self,
            name,
            family=None,
            brand=None,
            thermal_resistance_jb=None,
            reference_temperature=None,
            typical_voltage=None,
            typical_current=None,
            wavelength_vs_relative_spectral_emission=None,
            current_vs_voltage=None,
            current_vs_relative_luminous_flux=None,
            temperature_vs_relative_forward_voltage=None,
            temperature_vs_relative_luminous_flux=None):

        try:
            self.c.execute("INSERT INTO leds VALUES (NULL,?,NULL,NULL,NULL,NULL,NULL,NULL)", (name,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

        self.updateLed(
            name,
            family,
            brand,
            thermal_resistance_jb,
            reference_temperature,
            typical_voltage,
            typical_current,
            wavelength_vs_relative_spectral_emission,
            current_vs_voltage,
            current_vs_relative_luminous_flux,
            temperature_vs_relative_forward_voltage,
            temperature_vs_relative_luminous_flux)

    def updateLed(self,
            name,
            family=None,
            brand=None,
            thermal_resistance_jb=None,
            reference_temperature=None,
            typical_voltage=None,
            typical_current=None,
            wavelength_vs_relative_spectral_emission=None,
            current_vs_voltage=None,
            current_vs_relative_luminous_flux=None,
            temperature_vs_relative_forward_voltage=None,
            temperature_vs_relative_luminous_flux=None):

        if family is not None:
            pass

        if brand is not None:
            pass

        if thermal_resistance_jb is not None:
            pass

        if reference_temperature is not None:
            pass

        if typical_voltage is not None:
            pass

        if wavelength_vs_relative_spectral_emission is not None:
            pass

        if current_vs_voltage is not None:
            pass

        if current_vs_relative_luminous_flux is not None:
            pass

        if temperature_vs_relative_forward_voltage is not None:
            pass

        if temperature_vs_relative_luminous_flux is not None:
            pass

        self.conn.commit()


if __name__ == "__main__":
    db = LedDatabase()
    db.addBrand("OSRAM")
    db.addBrand("LUMILEDS")
    db.addFamily("TOPLED")
    db.addLed("LA T67F")
    db.addLed("LA T67F")
