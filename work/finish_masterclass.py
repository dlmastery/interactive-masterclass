import marimo_studio
v=marimo_studio.agent.current_workspace().view('lesson')
print(await v.validate(level='runtime'))
print(await v.show())
