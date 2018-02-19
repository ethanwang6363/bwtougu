import six

def compile_strategy(source_code, strategy, scope):
    try:
        code = compile(source_code, strategy, 'exec')
        six.exec_(code, scope)
        return scope
    except Exception as e:
        six.print_(e)
        raise e