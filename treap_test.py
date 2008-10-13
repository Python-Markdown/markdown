from markdown import Treap

if __name__ == '__main__':
    from pprint import pprint

    def test(t, b):
        if b is True:
            print t, "Passed"
        else:
            print t, "Failed"

    print "Testing..."
    r = Treap()
    r.add('first', 'This', '_begin')
    r.add('second', 'is', '>first')
    r.add('fourth', 'self', '>second')
    r.add('fifth', 'test', '>fourth')
    r.add('third', 'a', '>second')
    r['seventh'] = '.'

    print ".. Heapsort Test"
    test('.... vals', r.heapsorted() == ['This', 'is', 'a', 'self', 'test','.'])
    test('.... keys', r.heapsorted(keys=1) == ['first', 'second', 'third', 'fourth', 'fifth','seventh'])
    test('.... items', r.heapsorted(items=1) == [('first', 'This'), ('second', 'is'), ('third', 'a'), ('fourth', 'self'), ('fifth', 'test'), ('seventh','.')])

    print ".. Dict Storage Test"
    r._reset()
    test('.... vals', r.values() == r._vals)
    r._reset()
    test('.... keys', r.keys() == r._keys)
    r._reset()
    test('.... items', r.items() == r._items)

    print ".. Delete Node Test"
    del r['second']
    test('.... vals', r.heapsorted() == ['This', 'a', 'self', 'test','.'])
    test('.... keys', r.heapsorted(keys=1) == ['first', 'third', 'fourth', 'fifth','seventh'])
    test('.... items', r.heapsorted(items=1) == [('first', 'This'), ('third', 'a'), ('fourth', 'self'), ('fifth', 'test'), ('seventh','.')])

    print ".. Change value test."
    r['seventh'] = 'CRAZY'
    test('.... vals', r.heapsorted() == ['This', 'a', 'self', 'test','CRAZY'])
    test('.... keys', r.heapsorted(keys=1) == ['first', 'third', 'fourth', 'fifth','seventh'])
    test('.... items', r.heapsorted(items=1) == [('first', 'This'), ('third', 'a'), ('fourth', 'self'), ('fifth', 'test'), ('seventh','CRAZY')])
    print ".. Change priority test."
    r.link('seventh', '<third')
    test('.... vals', r.heapsorted() == ['This', 'a', 'self', 'CRAZY', 'test'])
    test('.... keys', r.heapsorted(keys=1) == ['first', 'third', 'fourth','seventh', 'fifth'])
    test('.... items', r.heapsorted(items=1) == [('first', 'This'), ('third', 'a'), ('fourth', 'self'), ('seventh','CRAZY'), ('fifth', 'test')])

