test: clean build
	docker run -d -p 32001:22 --name host1 centos7
	docker run -d -p 32002:22 --name host2 centos7
	docker run -d -p 32003:22 --name host3 centos7
	docker run -d -p 32004:22 --name host4 centos7
	docker run -d -p 32005:22 --name host5 centos7

	echo "[all]" > hosts
	echo host1 ansible_port=32001 >> hosts
	echo host2 ansible_port=32002 >> hosts
	echo host3 ansible_port=32003 >> hosts
	echo host4 ansible_port=32004 >> hosts
	echo host5 ansible_port=32005 >> hosts
	echo host6 ansible_port=32006 >> hosts  # intentional unreachable

	ansible-playbook -i hosts test.yml

build:
	mkdir -p ./tmp
	cp ~/.ssh/id_dsa.pub ./tmp
	docker build -t centos7 -f Dockerfile .
	rm ./tmp/id_dsa.pub
	rmdir ./tmp/

clean:
	-docker rm -f host1
	-docker rm -f host2
	-docker rm -f host3
	-docker rm -f host4
	-docker rm -f host5
	rm -f test.retry
