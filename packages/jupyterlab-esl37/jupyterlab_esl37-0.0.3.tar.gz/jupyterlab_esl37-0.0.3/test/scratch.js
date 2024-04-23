import {parser} from "./src/parser.js"
import { printTree } from "@lezer-unofficial/printer"

var source = `
def func(a: int) -> int:
    switch CUR_TICK:
        {% for tick, value in somedata %}
        case {{ tick }}:
            return {{ value }}
        {% endfor %}
    end
end
`

var tree = parser.parse(source)

// console.log(tree.toString())
console.log(printTree(tree, source))

// select(vset1, uniform01)

