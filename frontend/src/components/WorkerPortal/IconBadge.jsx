import React from "react";
import { AlertTriangle, ShieldCheck, IndianRupee, ShieldAlert, ArrowDownCircle, Sparkles } from "lucide-react";

export const IconBadge = ({ iconType, className = "w-6 h-6" }) => {
  switch (iconType) {
    case "helmet":
      return <ShieldAlert className={`${className} text-amber-600`} />;
    case "money":
      return <IndianRupee className={`${className} text-emerald-600`} />;
    case "danger":
      return <AlertTriangle className={`${className} text-rose-600`} />;
    case "deduction":
      return <ArrowDownCircle className={`${className} text-amber-700`} />;
    case "bonus":
      return <Sparkles className={`${className} text-blue-600`} />;
    default:
      return <ShieldCheck className={`${className} text-sky-600`} />;
  }
};
