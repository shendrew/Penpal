export default function handler(req, res) {
  if (req == "POST") {
    const { angle, acceleration } = req.body;
    res.status(200).json({ angle, acceleration });
  }
}