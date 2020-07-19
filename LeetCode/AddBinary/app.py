class Solution:
    def addBinary(self, a: str, b: str) -> str:
        out = ""
        carry = 0

        while a or b or carry:
            if a:
                carry += (a[-1]=="1")
                a = a[:-1]
            if b:
                carry += (b[-1]=="1")
                b = b[:-1]

            out = ("1" if carry%2 else "0") + out
            carry //= 2

        return out
