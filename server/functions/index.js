const { onRequest } = require("firebase-functions/v2/https");
const { initializeApp } = require("firebase-admin/app");
const { getFirestore } = require("firebase-admin/firestore");

initializeApp();
const db = getFirestore();

exports.add_admin = onRequest(async (req, res) => {
  const userId = req.query.userId;
  if (!userId || typeof userId !== "string") {
    return res.status(400).send("missing or invalid userId");
  }
  try {
    const adminDoc = db.collection("admins").doc(userId);
    await adminDoc.set({ userId });
    res.status(201).end(`added user ${userId} as admin`);
  } catch (error) {
    res.status(500).json({ error });
  }
});

exports.remove_admin = onRequest(async (req, res) => {
  const userId = req.query.userId;
  if (!userId || typeof userId !== "string") {
    return res.status(400).send("missing or invalid userId");
  }
  try {
    const adminDoc = db.collection("admins").doc(userId);
    await adminDoc.delete();
    res.status(201).end(`removed user ${userId}'s admin status`);
  } catch (error) {
    res.status(500).json({ error });
  }
});

exports.register = onRequest(async (req, res) => {
  try {
    const { userId, callsign } = req.body;

    if (!userId) {
      return res.status(400).send("missing userId");
    }
    if (!callsign) {
      return res.status(400).send("missing callsign or name");
    }

    const userDoc = db.collection("users").doc(userId);
    // todo: process callsign
    await userDoc.set({ userId, callsign: callsign.toUpperCase() });
    res.status(201).end(`Registerd user ${userId} as ${callsign}`);
  } catch (error) {
    res.status(500).json({ error });
  }
});

// Remove user by id
exports.unregister = onRequest(async (req, res) => {
  try {
    const userId = req.query.userId;

    if (!userId) {
      return res.status(400).send("missing userId");
    }

    const userDoc = db.collection("users").doc(userId);
    await userDoc.delete();
    res.status(204).end(`Removed user ${userId}`);
  } catch (error) {
    res.status(500).json({ error });
  }
});

// Remove user by callsign/name
exports.remove_user = onRequest(async (req, res) => {
  try {
    const callsign = req.query.callsign;

    if (!callsign) {
      return res.status(400).send("missing callsign");
    }
    // Find user by callsign
    const snapshot = await db
      .collection("users")
      .where("callsign", "==", callsign)
      .get();

    if (snapshot.empty) {
      return res.status(404).send(`no user found with callsign ${callsign}`);
    }

    const userDoc = snapshot.docs[0].ref; // Get first match in query snapshot, then access the referenced document
    await userDoc.delete();
    res.status(204).end(`Removed ${callsign}`);
  } catch (error) {
    res.status(500).json({ error });
  }
});
