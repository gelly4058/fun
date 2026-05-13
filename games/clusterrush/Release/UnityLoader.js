function CompatibilityCheck() {
    hasWebGL ? mobile ? confirm("Please note that Unity WebGL is not currently supported on mobiles. Press Ok if you wish to continue anyway.") || window.history.back() : -1 == browser.indexOf("Chrome") && -1 == browser.indexOf("Safari") && (confirm("Please note that your browser is not currently supported for this Unity WebGL content. Press Ok if you wish to continue anyway.") || window.history.back()) : (alert("You need a browser which supports WebGL to run this content."), window.history.back())
}

function UnityErrorHandler(e, t, n) {
    return Module.errorhandler && Module.errorhandler(e, t, n) || (console.log("Invoking error handler due to\n" + e), "function" == typeof dump && dump("Invoking error handler due to\n" + e), didShowErrorMessage || -1 != e.indexOf("UnknownError") || -1 != e.indexOf("Program terminated with exit(0)")) ? void 0 : (didShowErrorMessage = !0, -1 != e.indexOf("DISABLE_EXCEPTION_CATCHING") ? void alert("An exception has occurred, but exception handling has been disabled in this build. If you are the developer of this content, enable exceptions in your project's WebGL player settings to be able to catch the exception or see the stack trace.") : -1 != e.indexOf("Cannot enlarge memory arrays") ? void alert("Out of memory. If you are the developer of this content, try allocating more memory to your WebGL build in the WebGL player settings.") : -1 != e.indexOf("Invalid array buffer length") || -1 != e.indexOf("Invalid typed array length") || -1 != e.indexOf("out of memory") ? void alert("The browser could not allocate enough memory for the WebGL content. If you are the developer of this content, try allocating less memory to your WebGL build in the WebGL player settings.") : void alert("An error occurred running the Unity content on this page. See your browser's JavaScript console for more info. The error was:\n" + e))
}

function demangleSymbol(e) {
    return Module.debugSymbols && Module.debugSymbols[e] && (e = Module.debugSymbols[e]), e.lastIndexOf("__Z", 0) || (e = (Module.demangle || demangle)(e)), e
}

function demangleError(e) {
    var t = -1 != browser.indexOf("Chrome") ? "(\\s+at\\s+)(([\\w\\d_\\.]*?)([\\w\\d_$]+)(/[\\w\\d_\\./]+|))(\\s+\\[.*\\]|)\\s*\\((blob:.*)\\)" : "(\\s*)(([\\w\\d_\\.]*?)([\\w\\d_$]+)(/[\\w\\d_\\./]+|))(\\s+\\[.*\\]|)\\s*@(blob:.*)",
        n = new RegExp(t, "g"),
        o = new RegExp("^" + t + "$");
    return e.replace(n, function(e) {
        var t = e.match(o),
            n = demangleSymbol(t[4]),
            i = t[7].match(/^(blob:.*)(:\d+:\d+)$/),
            a = i && Module.blobInfo && Module.blobInfo[i[1]] && Module.blobInfo[i[1]].url ? Module.blobInfo[i[1]].url : "blob";
        return t[1] + n + (t[2] != n ? " [" + t[2] + "]" : "") + " (" + (i ? a.substr(a.lastIndexOf("/") + 1) + i[2] : t[7]) + ")"
    })
}
