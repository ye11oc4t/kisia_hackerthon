const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// 설정을 config.json 파일에서 불러옴
const config = require('./config.json');

(async () => {
    const browser = await puppeteer.launch({ headless: config.headless });
    const page = await browser.newPage();

    // 다운로드 폴더 설정
    await page._client.send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: config.downloadsFolder
    });

    // 네트워크 요청 감지
    page.on('response', async response => {
        const contentDisposition = response.headers()['content-disposition'];
        if (contentDisposition && contentDisposition.indexOf('attachment') !== -1) {
            const downloadUrl = response.url();
            const filename = contentDisposition.split('filename=')[1].split(';')[0].replace(/\"/g, '');
            console.log(`다운로드 감지됨: 파일명 - ${filename}`);

            // 다운로드 중단 및 파일 삭제
            await response.cancel();
            const filePath = path.join(config.downloadsFolder, filename);
            if (fs.existsSync(filePath)) {
                fs.unlinkSync(filePath);
                console.log(`${filename} 파일이 삭제되었습니다.`);
            }
        }
    });

    // targetUrl로 이동
    await page.goto(config.targetUrl, { waitUntil: 'networkidle0' });

    // 추가 대기 시간
    await page.waitForTimeout(config.waitTime); // config.json에서 설정한 시간 동안 대기

    await browser.close();
})();
