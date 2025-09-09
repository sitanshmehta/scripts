//purpose - waterloo works doesnt let users bull delete rows anymore. This is script can be pasted 
// into the console to delete multiple rows at once

//Flow - loop through the table, if a row is selected, click the "dnd" button, then click delete in the popup
//repeat until all selected rows are deleted (might be a problem since table updates after each deletion / pagnication)

let ROWS_LEFT_TO_DELETE = true;

const getTableRows = () => {
    return document.querySelectorAll('table tbody tr');
}

const isRowSelected = row => {
    return row.querySelector('input[type="checkbox"]:checked');
}

const findRowRemoveBtn = row =>
    row.querySelector('button[aria-label="Remove from search results"]');

const findConfirmBtn = () =>
    document.querySelector('button.btn--error, button.btn__default--text.btn--error');

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function deleteRows() {
    const rows = Array.from(getTableRows()).filter(isRowSelected);
    const length = rows.length;
    if (length == 0) {
        ROWS_LEFT_TO_DELETE = false;
    }
    for (let i = 0; i < length; i++) {
        const removeBtn = findRowRemoveBtn(rows[i]);
        removeBtn.click();
        await sleep(100);
        const confirmRemoveBtn = findConfirmBtn();
        confirmRemoveBtn.click();
        await sleep(100);
        console.log("Length: ", rows.length, "Index: ", i);
    }
}

async function main() {
    for (let i = 0; i < 10; i++) {
        await deleteRows();
        if (!ROWS_LEFT_TO_DELETE) {
            return;
        }
        sleep(1000);
    }
}

await main();


