import {styleTags, tags} from "@lezer/highlight"

export const highlight = styleTags({
    Reference: tags.variableName,
    VariableName: tags.variableName,
    TypeName: tags.typeName,
    FunctionName: tags.function(tags.variableName),
    ConstantName: tags.constant(tags.variableName),

    Integer: tags.integer,
    Float: tags.float,
    Boolean: tags.bool,
    String: tags.string,
    Comment: tags.lineComment,
    FieldAnnotation: tags.annotation,
    StateTypeAnnotation: tags.annotation,

    TemplateBlock: tags.special(tags.lineComment),
    TemplateVar: tags.meta,

    "enum global config node edge": tags.definitionKeyword,
    "distribution discrete normal uniform": tags.definitionKeyword,
    "contagion transition transmission": tags.definitionKeyword,

    "p v mean std low high dwell": tags.keyword,
    "susceptibility infectivity transmissibility enabled": tags.keyword,

    "nodeset edgeset": tags.definitionKeyword,
    "def end var": tags.definitionKeyword,
    "pass return if elif else switch case default while": tags.controlKeyword,
    "select sample apply reduce": tags.controlKeyword,

    '"+" "-" "*" "/"': tags.arithmeticOperator,
    "and or not": tags.logicOperator,
    '"==" "!=" ">" ">=" "<" "<="': tags.compareOperator,
    '"=" "*=" "/=" "%=" "+=" "-="': tags.updateOperator,
    '":" "," "=>" "->" "<-"': tags.punctuation,
    '"."': tags.separator,

    "( )": tags.paren,
    "{ }": tags.brace,
    "[ ]": tags.squareBracket
})
