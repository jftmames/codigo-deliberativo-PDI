from typing import List
class InquiryEngine:
    def __init__(self, root_question: str):
        self.root = root_question
    def generate(self) -> List[str]:
        return [self.root]
