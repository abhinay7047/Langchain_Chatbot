from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Student(BaseModel):
    name: str = 'John Doe'
    age: Optional[int] = None 
    roll: Optional[int] = None
    email: Optional[EmailStr] = None
    Cgpa : Optional[float] = Field(None,ge=0,le=10, description="CGPA of student")

new_student={"name":'John',"age":20,"roll":101,"email":"abs@gmail.com", 'cgpa':9.5}
student = Student(**new_student)
student_dict=dict(student)
print(student_dict['age'])