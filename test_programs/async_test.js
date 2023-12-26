// Probando el asincronismo de javascript

const a = 1
const b = 2
let c = 0

async function sum() {
    c += a + b
    console.log("terminando c vale ", c)
}

async function main() {
    sum()
    sum()
    sum()
    console.log("c vale ", c)
}

main()
console.log("Final c vale: ", c)
