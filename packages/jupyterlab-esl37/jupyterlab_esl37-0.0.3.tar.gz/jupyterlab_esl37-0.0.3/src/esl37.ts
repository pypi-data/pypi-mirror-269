import {LRLanguage, LanguageSupport} from "@codemirror/language"
import {parser} from "./parser"

export const esl37Language = LRLanguage.define({
    name: "esl37",
    parser: parser.configure({
        props: []
    }),
    languageData: {
        closeBrackets: {
            brackets: [],
            stringPrefixes: []
        },
        commentTokens: {},
    }
})

export function esl37() {
    try {
        return new LanguageSupport(esl37Language, [])
    } catch (error) {
        console.error(error)
        throw error;
    }
}
