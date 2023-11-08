const { onRequest } = require("firebase-functions/v2/https");
const { initializeApp } = require("firebase-admin/app");
const { getFirestore } = require("firebase-admin/firestore");

initializeApp();
const db = getFirestore();

exports.get_users = onRequest(async (req, res) => {
  try {
    const usersSnapshot = await db.collection("users").get();
    const users = usersSnapshot.docs.map((doc) => doc.data());
    res.json(users);
  } catch (error) {
    res.status(500).json({ error });
  }
});

exports.get_admins = onRequest(async (req, res) => {
  try {
    const adminsSnapshot = await db.collection("admins").get();
    const admins = adminsSnapshot.docs.map((doc) => doc.data());
    res.json(admins);
  } catch (error) {
    res.status(500).json({ error });
  }
});

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

// For users to register themselves with their callsigns
exports.register = onRequest(async (req, res) => {
  try {
    const userId = req.query.userId;
    const callsign = req.query.callsign;

    if (!userId || typeof userId !== "string") {
      return res.status(400).send("missing or invalid userId");
    }
    if (!callsign || typeof callsign !== "string") {
      return res.status(400).send("missing callsign or name");
    }

    const formattedCallsign = callsign.toUpperCase().split("_").join(" ");

    const userDoc = db.collection("users").doc(userId);
    await userDoc.set({
      userId,
      callsign: formattedCallsign,
    });
    res.status(201).end(`Registered user ${userId} as ${formattedCallsign}`);
  } catch (error) {
    res.status(500).json({ error });
  }
});

// For users to unregister themselves
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

// For admins to remove users by their callsign
exports.remove_user = onRequest(async (req, res) => {
  const callsign = req.query.callsign;
  if (!callsign || typeof callsign !== "string") {
    return res.status(400).send("missing callsign or name");
  }

  const formattedCallsign = callsign.toUpperCase().split("_").join(" ");

  try {
    // Find user by callsign
    const snapshot = await db
      .collection("users")
      .where("callsign", "==", formattedCallsign)
      .get();

    if (snapshot.empty) {
      return res
        .status(404)
        .send(`no user found with callsign or name ${formattedCallsign}`);
    }

    const userDoc = snapshot.docs[0].ref; // Get first match in query snapshot, then access the referenced document
    await userDoc.delete();
    res.status(204).end(`Removed ${formattedCallsign}`);
  } catch (error) {
    res.status(500).json({ error });
  }
});
