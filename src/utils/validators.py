"""Validátory vstupů"""
import re


class Validators:
    """Třída pro validaci vstupů"""
    
    @staticmethod
    def validate_email(email):
        """Validuje email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_price(price):
        """Validuje cenu"""
        try:
            p = float(price)
            return p > 0
        except:
            return False
    
    @staticmethod
    def validate_phone(phone):
        """Validuje telefonní číslo"""
        if not phone:
            return True
        pattern = r'^[\d\s\-\+\(\)]{9,}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_postal_code(psc):
        """Validuje poštovní směrovací číslo"""
        pattern = r'^\d{3}\s?\d{2}$'
        return re.match(pattern, psc) is not None
    
    @staticmethod
    def validate_positive_int(value):
        """Validuje kladné celé číslo"""
        try:
            return int(value) > 0
        except:
            return False
    
    @staticmethod
    def validate_enum(value, allowed):
        """Validuje hodnotu z výčtu"""
        return value in allowed
