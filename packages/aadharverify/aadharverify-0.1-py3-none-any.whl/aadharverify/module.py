class Verhoeff:
    """Verhoeff algorithm for checksum calculation and validation."""
    d = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
         [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
         [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
         [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
         [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
         [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
         [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
         [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
         [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
         [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]

    # Permutation table    
    p = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
         [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
         [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
         [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
         [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
         [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
         [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
         [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]

    # Inverse table    
    inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

    @classmethod
    def calculate(cls, num):
        """Calculate the Verhoeff checksum digit for the given number."""        
        c = 0        
        num = num[::-1]
        for i in range(len(num)):
            c = cls.d[c][cls.p[i % 8][int(num[i])]]
        return cls.inv[c]
    
    @classmethod
    def validate(cls, num):
        """Validate the given number with its checksum digit."""        
        c = 0
        num = num[::-1]
        for i in range(len(num)):
            c = cls.d[c][cls.p[(i + 1) % 8][int(num[i])]]
        return c == 0
    
    def verify_aadhar(aadhar_number):
        """Verify if the provided Aadhar number is valid."""    
        aadhar_str = str(aadhar_number)
        if len(aadhar_str) != 12 or not aadhar_str.isdigit():
            return False
        return Verhoeff.validate(aadhar_str)