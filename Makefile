@all:
	python -m build --wheel --no-isolation

install:
	python -m installer --destdir="${DESTDIR}" dist/*.whl
	mkdir -p ${DESTDIR}/usr/share/python-cassandra
	cp -r skel ${DESTDIR}/usr/share/python-cassandra
	cp config.yaml ${DESTDIR}/usr/share/python-cassandra/
