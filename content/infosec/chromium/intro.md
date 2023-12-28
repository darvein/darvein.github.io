# Introduction to Google Chrome

Based browsers based in chromium:

- Brave browser
- Vivaldi
- Edge
- Steam

Chrome uses: apple webkit, mozilla firefox? and part of chromium project
  - google foked webkit and named it Blink Engine


## Techniques of explotations
- Semantic Equivalent Transform (SET): program transforming JS seed generates new JSes
  - translates: a.js -> (ast, mutate) -> b.js
    - builtins, methods, scope, variable, type, signature
    - loopenize (for, while), functionize, empty loop, garbage collection, nontype based, conditionize, repeat
  - fuzzers?
- Advanced Exploitation Techinque
  - OOB Exploitation
    - Leak ArrayBuffer backing store
  - V8 out-of-bound in Promise
- Chrome Sandbox Bypass
  - Logical bug
    - attack renderer
    - attack webview in privileged app
  - Kernel
    - win32k lockdown
    - CLFS
  - Memory Corruption via IPC
    - UAF scape sandbox
      - indexedDB (api in browser?)
    - IndexedDB IPC interfaces: IDBFactory, IDBDatabase, IDBCursor
- Exploiting in windows
  - limitations
    - no CFG, many virtual function calls in C++, all we need is heap adddress to put ROP
- ChromeOS
  - Clang CFI enabled is different
  - no libs and library address
- Renderer process
- Valid vulns for reward:
  - sandbox scape
  - renderer RCE
  - universal XSS (local bypass or equivalent)
  - information leak

## Rock stars?
- Zhen Feng
- Gengming Liu

## Common vulns
- CVE-2020-16001: UAF in media : Khali Zhani
- CVE-2020-16002: UAF in PDFium : Weipeng Jiang
- CVE-2020-15999: heap overflow in Freetype : Sergei Glazunov
- CVE-2016-5129: (TODO: Need to review this one)
- CVE-2016-0193: (TODO: Need to review this one)
- CVE-2016-5198: (TODO: Need to review this one)
- CVE-2017-5053: out-of-bound access capability
- CVE-2016-5197: arbitrary intent start in renderer
- CVE-2019-5826: UAF in IndexedDB
- CVE-2021-37975: v8 engine vuln
- CVE-2021-37976: information leak in core
- CVE-2021-37973: Use after free in Portals
- CVE-2021-30632 & CVE-2021-30633: by anonymouse: use after free in Indexed DB API
- CVE-2021-31956 is a Windows NTFS Elevation of Privilege (EoP) vulnerability
  - CVE-2021-21224 to escape the Chromium sandbox
  - called PuzzleMaker by Kaspersky
  - Windows builds 18362, 18363, 19041, and 19042 (19H1–20H2). Build 19043 (21H1) is not targeted
    - has harcoded syscalls
  - Magnitude exploit kit (EK)
- CVE-2021-30573: UAF in GPU
- CVE-2021-21220: pwn2own

## chrome possible cves from 2021
CVE-2021-21148 – February 4th, 2021
CVE-2021-21166 – March 2nd, 2021
CVE-2021-21193 – March 12th, 2021
CVE-2021-21220 – April 13th, 2021
CVE-2021-21224 – April 20th, 2021
CVE-2021-30551 – June 9th, 2021
CVE-2021-30554 – June 17th, 2021
CVE-2021-30554 – June 17th, 2021
CVE-2021-30563 – July 15th, 2021
CVE-2021-30632 & CVE-2021-30633 – Sept 13th, 2021
CVE-2021-37973 – Sept 24th, 2021
CVE-2021-37975 and CVE-2021-37976 – Oct, 13st, 2021


## References
- Defcon talk "The Most Secure Browser? Pwning Chrome from 2016 to 2019": https://www.youtube.com/watch?v=OoL9nyu-f-Q&t=1738s
- https://github.com/0xcl
- Chrome security page: https://sites.google.com/a/chromium.org/dev/Home/chromium-security
- Chrome releases page: https://chromereleases.googleblog.com/
- Hall of fame: https://sites.google.com/a/chromium.org/dev/Home/chromium-security/hall-of-fame
- Chrome vulnerability reward program: https://bughunters.google.com/about/rules/5745167867576320
- Source code: https://source.chromium.org/chromium
  - Chromium source code structure: https://www.chromium.org/developers/how-tos/getting-around-the-chrome-source-code
- Chromium for developers: https://www.chromium.org/developers
- Web browser anatomy: https://www.youtube.com/watch?v=PzzNuCk-e0Y

## More references
- Game of Chromes: Owning the Web with Zombie Chrome Extensions: https://www.youtube.com/watch?v=UHwpusw6mPc
- https://www.youtube.com/watch?v=pkIBnDJPluY
- https://www.youtube.com/watch?v=DFPD9yI-C70
- https://www.youtube.com/watch?v=PlCu1NBuU4I
- https://www.youtube.com/watch?v=vn7YIAiOnYw
- https://en.wikipedia.org/wiki/Google_Chrome
- https://medium.com/swlh/my-take-on-chrome-sandbox-escape-exploit-chain-dbf5a616eec5
- https://googleprojectzero.blogspot.com/2019/04/virtually-unlimited-memory-escaping.html
- https://bugs.chromium.org/p/project-zero/issues/detail?id=1755
- https://dev.chromium.org/developers/design-documents/multi-process-architecture
- https://docs.google.com/document/d/1aitSOucL0VHZa9Z2vbRJSyAIsAz24kX8LFByQ5xQnUg/edit
- https://github.com/vngkv123/aSiagaming/tree/master/Chrome-v8-906043
- https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/mojo/README.md
- https://seclab.stanford.edu/websec/chromium/chromium-security-architecture.pdf
- https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=chrome
- https://v8.dev/docs/profile-chromium
- https://securitylab.github.com/research/chromium-ipc-vulnerabilities/
- https://googleprojectzero.blogspot.com/2019/04/virtually-unlimited-memory-escaping.html
- https://www.powerofcommunity.net/poc2018/ned.pdf
- https://bugs.chromium.org/p/project-zero/issues/detail?id=1942#c7
- https://developers.google.com/web/updates/2018/09/inside-browser-part1
- https://zicodeng.medium.com/explore-the-magic-behind-google-chrome-c3563dbd2739
- https://www.chromium.org/developers/how-tos/get-the-code
- what are the chrome CVES in 2021?
- google chrome security page: https://sites.google.com/a/chromium.org/dev/Home/chromium-security
- chaining exploits: https://github.blog/2021-03-24-real-world-exploit-chains-explained/
  - https://securitylab.github.com/research/one_day_short_of_a_fullchain_sbx/
  - https://securitylab.github.com/advisories/GHSL-2020-165-chrome/
- https://github.com/obezuk/chrome-0day
- https://github.com/RedWifiTeam/Chrome-0Day-EXP
- https://github.com/AeolusTF/chrome-0day
- https://github.com/H4ckTh3W0r1d/Chrome-0day
- https://github.com/77409/chrome-0day
- build chromium: https://www.youtube.com/watch?v=jeRKirsUq4k
- anatomy of a web browser: https://www.youtube.com/watch?v=PzzNuCk-e0Y
- IPC: https://www.youtube.com/watch?v=MMxtKq8UgwE
- https://www.youtube.com/watch?v=0uejy9aCNbI
- https://www.youtube.com/watch?v=y6Uzinz3DRU

## CVE videos
- Security researcher drops Chrome 0day exploit on Twitter, new xorg-server CVE & how was your day?: https://www.youtube.com/watch?v=6qNjVGpl-fI
- https://www.youtube.com/watch?v=7mqPDFb2svc
- https://www.youtube.com/watch?v=IRm3R-Gejcc

## Interesting
- Check latest issues in chrome: https://bugs.chromium.org/p/chromium/issues/list?q=type%3Abug-security%20os%3DAndroid%2Cios%2Clinux%2Cmac%2Cwindows%2Call%2Cchrome&can=1

## Exploitation mitigations
- aslr
- r-x
- hardened heap
