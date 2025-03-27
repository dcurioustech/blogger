from blog_writer import generate_blog_post 
def test_blog_writer_functionality():
    generate_blog_post("Machine Learning")

# pytest.ini
[pytest]
addopts = -v
