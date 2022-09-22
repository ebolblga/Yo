const fs = require("fs");
let words1 = fs.readFileSync("./Data/russianUTF-8.txt").toString();
words1 = words1.split("\n");
if (words1.length && words1[0].at(-1) == "\r")
  words1 = words1.map((word) => word.slice(0, -1));

let words2 = fs.readFileSync("./Data/summary.txt").toString();
words2 = words2.split("\n");
if (words2.length && words2[0].at(-1) == "\r")
  words2 = words2.map((word) => word.slice(0, -1));

let output = "";
let searchWord = "";
for (let i = 0; i < words1.length; i++) {
  if (/ё/gi.test(words1[i])) {
    searchWord = words1[i].replace("ё", "е");

    for (let j = 0; j < words2.length; j++) {
      if (searchWord == words2[j]) {
        output += "| " + words1[i] + " | " + words2[j] + " |\n";
      }
    }
  }
}

fs.writeFileSync("./Data/Output.txt", output);