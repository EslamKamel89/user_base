class Validate():
    @classmethod
    def strip_and_validate_name(cls , v:str|None , min:int = 2)->str|None : 
        if v is None :
            return None
        v = v.strip()
        if not v or len(v) < min :
            raise ValueError(f'name must be at least {min} chars')
        return v
    
    @classmethod
    def strip_lower_validate_email(cls , v:str|None)->str|None : 
        if v is None :
            return None
        v = v.strip().lower()
        if '@' not in v or '.' not in v :
            raise ValueError('invalid email format')
        return v
    
    @classmethod
    def validate_password(cls , val:str) :
        if len(val) < 5 : 
            raise ValueError('password must be at least 5 chars')
        return val