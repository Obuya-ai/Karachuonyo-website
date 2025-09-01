// Google Apps Script: webhook to append form submissions to Google Sheet
function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
    if(!sheet) {
      sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Sheet1');
      sheet.appendRow(['Timestamp','Name','Email','Phone','Message','Target']);
    }
    var payload = JSON.parse(e.postData.contents);
    sheet.appendRow([new Date(), payload.name || '', payload.email || '', payload.phone || '', payload.message || '', payload.target || '']);
    return ContentService.createTextOutput(JSON.stringify({status:'ok'})).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({status:'error', error: err.toString()})).setMimeType(ContentService.MimeType.JSON);
  }
}
