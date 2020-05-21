print("Hello, ch06 of python_book")

# 최상위 object class 를 명시적으로 표기하는 것을 권장
class Point(object):
    # Point class represents and manipulates x, y coords.
    def __init__(self):
        # Create a new point at the origin
        self.x = 0
        self.y = 0

def test_create_class_instance():
    p = Point()
    q = Point()
    print("test+test_create_class_instance", p.x, p.y, q.x, q.y)


#####################################

if __name__ == "__main__":
    test_create_class_instance()
