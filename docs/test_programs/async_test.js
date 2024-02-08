// Probando el asincronismo de javascript

const a = 1
const b = 2
let c = 0

async function sum() {
    c += a + b
}

async function main() {
    await sum()
    await sum()
}

main()
console.log("Final c vale: ", c)
