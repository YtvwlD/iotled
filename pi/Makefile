install:
	mkdir -p /usr/lib/iotled
	cp *.py /usr/lib/iotled
	cp iotled.service /lib/systemd/system/
	systemctl daemon-reload
	systemctl enable --now iotled.service

uninstall:
	rm -rf /usr/lib/iotled
	rm /lib/systemd/system/iotled.service
	rm /lib/systemd/system/multi-user.target.wants/iotled.service
