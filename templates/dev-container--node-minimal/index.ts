#!/usr/bin/env ts-node

import {
    transpileModule,
    ModuleKind,
} from "typescript";

const tsCode = "const x: number = 10;";
const result = transpileModule(tsCode, {
    compilerOptions: {
        module: ModuleKind.CommonJS,
    },
});

console.log(result.outputText);
