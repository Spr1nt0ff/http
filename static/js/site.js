document.addEventListener('DOMContentLoaded', () => {
    initApiTests();
});


class Base64 {
    static #textEncoder = new TextEncoder();
    static #textDecoder = new TextDecoder();

    static decodeUrl = (str) => this.#textDecoder.decode(Uint8Array.from(atob(str.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0)));
    static jwtDecodeHeader = (jwt) => JSON.parse(this.decodeUrl(jwt.split('.')[0]));

    static validateClaims(payload) {
        const errors = [];
        const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!payload.sub || !uuidRegex.test(payload.sub)) {
            errors.push("sub must be a valid UUID");
        }

        if (payload.iss !== "Server-KN-P-221") {
            errors.push("iss must be 'Server-KN-P-221'");
        }

        if (!payload.name && !payload.email) {
            errors.push("Token must contain at least 'name' or 'email'");
        }

        if (payload.email && !emailRegex.test(payload.email)) {
            errors.push("Invalid email format");
        }

        return errors;
    }

    static jwtProcess(jwt) {
        const header = this.jwtDecodeHeader(jwt);

        if (header.cty === "JWT") {
            console.log("Detected nested JWT (cty: JWT). Returning to Step 1...");
            const rawPayload = this.decodeUrl(jwt.split('.')[1]);
            const payloadObj = JSON.parse(rawPayload);
            const innerJwt = payloadObj.wrapped || rawPayload;
            return this.jwtProcess(innerJwt);
        }

        const payload = JSON.parse(this.decodeUrl(jwt.split('.')[1]));
        
        // Викликаємо валідацію Claims
        const validationErrors = this.validateClaims(payload);

        return {
            header: header,
            payload: payload,
            errors: validationErrors // Додаємо список помилок до результату
        };
    }
}

function initApiTests() {
    const apiNames = ["user", "order", "discount"];
    const apiMethods = ["get", "post", "put", "patch", "delete"];
    for (let apiName of apiNames) {
        for (let apiMethod of apiMethods) {
            let btnId = `api-${apiName}-${apiMethod}-btn`;
            let btn = document.getElementById(btnId);
            if (btn) {
                btn.addEventListener('click', apiTestBtnClick);
            }
        }
    }
}


function apiTestBtnClick(e) {
    const [prefix, apiName, apiMethod, _] = e.target.id.split('-');
    const resId = `${prefix}-${apiName}-${apiMethod}-result`;
    const td = document.getElementById(resId);

    if (td) {
        fetch(`/${apiName}`, {
            method: apiMethod.toUpperCase(),
            headers: { "Authorization": "Basic YWRtaW46YWRtaW4=" }
        }).then(r => {
            if (r.ok) {
                r.json().then(j => {
                    const result = Base64.jwtProcess(j.data);
                    
                    document.getElementById("token").innerHTML = j.data;
                    document.getElementById("token-header").innerHTML = 
                        `<b>Final Header:</b><pre>${JSON.stringify(result.header, null, 4)}</pre>`;
 
                    let errorHtml = "";
                    if (result.errors.length > 0) {
                        errorHtml = `<div style="color: #bf616a; margin-bottom: 10px;">
                            <b>Validation Errors:</b>
                            <ul>${result.errors.map(e => `<li>${e}</li>`).join('')}</ul>
                        </div>`;
                    }

                    document.getElementById("token-payload").innerHTML = 
                        `${errorHtml}<b>Final Payload:</b><pre>${JSON.stringify(result.payload, null, 4)}</pre>`;
                });
            } else {
                r.text().then(t => td.innerText = t);
            }
        });
    }
}
