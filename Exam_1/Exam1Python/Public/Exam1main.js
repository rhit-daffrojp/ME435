async function sendCommand(command) {
    var response = await fetch(`/api/${command}`);
    var replyText = await response.text();
    console.log(`Reply: ${replyText}`);

    document.querySelector("#replyText").innerHTML = replyText;

    return replyText;
}

function main() {
    console.log("Hello, JavaScript!!");
    
    document.querySelector("#on").onclick = () => {
        sendCommand("LED ON");
    }

    document.querySelector("#off").onclick = () => {
        sendCommand("LED OFF");
    };

    document.querySelector("#flash").onclick = () => {
        let num = document.querySelector("#NumFlashes").value;
        let per = document.querySelector("#PeriodMs").value;
        sendCommand(`FLASH ${num} ${per}`);
    };
}

main();
