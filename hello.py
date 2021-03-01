from textx import metamodel_from_file

hello_mm = metamodel_from_file('hello.tx')

hello_model = hello_mm.model_from_file('example.hello')

for who in hello_model.to_greet:
    print(f"Hello, {who.name}!")


