const dateId = "ContentPlaceHolder1_tabContainerReceipts_tabTabDetails_txtReceiptReceivedDate"
const receiptType = "ContentPlaceHolder1_tabContainerReceipts_tabTabDetails_ddlReceiptType"
const amount = "ContentPlaceHolder1_tabContainerReceipts_tabTabDetails_txtReceiptAmount"
const receivedFrom = "ContentPlaceHolder1_tabContainerReceipts_tabTabDetails_txtRcvdFrom"
const saveButton = "ContentPlaceHolder1_btnSave"
const formFields = [receiptType, dateId, amount, receivedFrom]

const fieldMap = {
	"ContentPlaceHolder1_tabContainerReceipts_tabTabDetails_ddlReceiptType": "type",
	"ContentPlaceHolder1_tabContainerReceipts_tabTabDetails_txtReceiptReceivedDate": "date",
	"ContentPlaceHolder1_tabContainerReceipts_tabTabDetails_txtReceiptAmount": "amount",
	"ContentPlaceHolder1_tabContainerReceipts_tabTabDetails_txtRcvdFrom": "received_from",
}

const receipts = [{'type': 'Individual Contribution', 'date': '07/02/2024', 'amount': '27.00', 'received_from': 'Dellutri, Aaron - 4423 N Rockwell St, Chicago, IL'}]

const fill_in_data = (receipts, formFields) => {
	for (let receipt of receipts) {
		for (let field of formFields) {
			let fieldElement = document.getElementById(field)
			fieldElement.setAttribute("value", receipt[fieldMap[field]])
		}
			button = document.getElementById(saveButton)
			button.click()
	}
}
