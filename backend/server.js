import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import documentRoutes from "./routes/documents.js";
import comprehensionRoutes from "./routes/comprehension.js";
import whatsappRoutes from "./routes/whatsapp.js";
import analyticsRoutes from "./routes/analytics.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.use("/api/documents", documentRoutes);
app.use("/api/comprehension", comprehensionRoutes);
app.use("/api/whatsapp", whatsappRoutes);
app.use("/api/analytics", analyticsRoutes);

app.get("/health", (req, res) => {
  res.json({ status: "ok", app: "ShiftMitra Backend", timestamp: new Date() });
});

app.listen(PORT, () => {
  console.log(`[ShiftMitra] Backend Server running on http://localhost:${PORT}`);
});
