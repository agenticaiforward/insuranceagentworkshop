import unittest
from memory import MemoryStore

class TestMemoryStore(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore()
        self.session_id = "test_session"
        self.fake_chat = "chat_object"

    def test_set_and_get(self):
        self.store.set(self.session_id, self.fake_chat)
        retrieved = self.store.get(self.session_id)
        self.assertEqual(retrieved, self.fake_chat)

    def test_clear(self):
        self.store.set(self.session_id, self.fake_chat)
        self.store.clear(self.session_id)
        self.assertIsNone(self.store.get(self.session_id))

if __name__ == "__main__":
    unittest.main()
