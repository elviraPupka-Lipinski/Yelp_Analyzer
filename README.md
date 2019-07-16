# Dataset
Download the data from https://www.yelp.com/dataset/challenge and place all files in the /app folder.

# Docker Build
The command to build the container. 
```bash
docker build --tag yelp-analyzer ./
```

# Docker Run
This starts the analyzer, where <ID> is the BusinessID to be analyzed. Default is c0yPNU-BqS65u0vIKP7P0w.
```bash
docker run -it yelp-analyzer --businessID <ID>
```

# List of some possible IDs
* c0yPNU-BqS65u0vIKP7P0w
* hDD6-yk1yuuRIvfdtHsISg
* dQj5DLZjeDK3KFysh1SYOQ
* qHseX2NHeUUedIgs_VasZA
* hzyvL2v97xLzLbLXcdi1uw
* X8AGCsJHw-GuTqkzy2J3cg
* Mv7N0bU56dhtoDP-m2JOow
* uRybQLCYWkC6N19MhaHf_w
* sMzNLdhJZGzYirIWt-fMAg
* 7z2x16M7IuG8KPfMsyVrKA
* 3TrY8CpsnvnTTYigx2R4yg
* nlVjdQq9FzdQ3bfy-8y80g