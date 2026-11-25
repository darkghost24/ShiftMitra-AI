export const processDocumentOcr = async (file, textHint) => {
  if (textHint && textHint.trim().length > 0) {
    return textHint;
  }

  const filename = file ? file.originalname.toLowerCase() : "";

  if (filename.includes("safety") || filename.includes("helmet")) {
    return `SAFETY MANDATE NOTICE - SHOP FLOOR ZONE 4
    All contract & regular workers must wear ISI mark safety helmets and steel-toe boots before entering.
    First violation penalty: Rs. 500 deducted directly from wages.
    Second violation: 3 days suspension without pay.
    Helmets must remain strapped at all times.
    Issued by: HSE Department, Apex Auto Components Ltd.`;
  }

  if (filename.includes("payslip") || filename.includes("salary")) {
    return `MONTHLY PAYSLIP - OCT 2026
    Worker: Ramesh Kumar | ID: W-4089 | Shift: B
    Basic Wage: Rs. 14,500
    Overtime (28 hrs @ 2x rate): Rs. 3,850
    Gross Salary: Rs. 18,350
    Deductions:
    - Provident Fund (PF 12%): Rs. 1,740
    - ESI Medical Insurance: Rs. 138
    - Canteen Mess Charges: Rs. 650
    Total Deductions: Rs. 2,528
    Net Take-Home Pay: Rs. 15,822 (Credited on 7th)`;
  }

  return `FACTORY HEALTH AND WELFARE ANNOUNCEMENT
  Free vaccination camp on Saturday 10 AM at Health Centre.
  Overtime shift on Sunday will be paid at double rate for all attending workers.
  Report to Supervisor before Friday 5 PM.`;
};
