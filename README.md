# hackerthon_team9_backend

주제 : 정하는중

### 1 - 1 로컬 환경에서 테스트 하는방법
make install - <패키지 의존성 설치해줌>

brew install direnv

-- 버전확인 -- <br>
direnv version

---
<h5> BASH -> ~/.bashrc에 아래 내용 추가 </h5>
eval "$(direnv hook bash)"

---
<h5> ZSH -> ~/.zshrc에 아래 내용 추가 </h5>
eval "$(direnv hook zsh)"

---
direnv allow

make run - <장고 프로젝트 실행>

### 2 - 1 git push 전

명렴프롬포트, 터미널 : make lint

lint 작업 시 import 부분에서 오류가 나왔다고 콘솔창에 뜬다면 # noqa  주석달고 무시하자

문법 검사하고 규격에 맞게 수정진행
