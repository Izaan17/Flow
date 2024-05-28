
def bind_all(parent, sequence: str, command):
    for child in parent.winfo_children():
        child.bind(sequence, command)
        bind_all(child, sequence, command)
