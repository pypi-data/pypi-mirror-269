default:
	@echo 'Targets:'
	@echo '  all'
	@echo '  test-easter'
	@echo '  test-day-number'
	@echo '  test-julian'
	@echo '  test-time'
	@echo '  test-coordinate'
	@echo '  test-sun'
	@echo '  test-planet-comet-binary'
	@echo '  test-moon'
	@echo '  test-eclipses'
	@echo '  build'
	@echo '  upload'

all: test-easter test-day-number test-julian test-time test-coordinate test-sun test-planet-comet-binary test-moon test-eclipses

test-easter:
	@./test_date_of_easter.py -v

test-day-number:
	@./test_day_number.py

test-julian:
	@./test_julian.py

test-time:
	@./test_time.py

test-coordinate:
	@./test_coordinate.py

test-sun:
	@./test_sun.py

test-planet-comet-binary:
	@./test_planet_comet_binary.py

test-moon:
	@./test_moon.py

test-eclipses:
	@./test_eclipses.py

build:
	python3 -m build

upload:
	python3 -m twine upload --repository testpypi dist/*
