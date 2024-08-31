// EmailPage.tsx

import React, { useState } from "react";

type Email = {
  id: number;
  sender: string;
  subject: string;
  body: string;
  date: string;
};

const sampleEmails: Email[] = [
  {
    id: 1,
    sender: "john@example.com",
    subject: "Meeting Reminder",
    body: "Don't forget about the meeting at 3 PM.",
    date: "Aug 30, 2024",
  },
  {
    id: 2,
    sender: "jane@example.com",
    subject: "Project Update",
    body: "Here is the latest update on the project...",
    date: "Aug 29, 2024",
  },
  {
    id: 3,
    sender: "team@example.com",
    subject: "Weekly Report",
    body: "Please review the attached weekly report.",
    date: "Aug 28, 2024",
  },
];

const EmailPage: React.FC = () => {
  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null);

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-md-2 bg-light border-end">
          <h5 className="p-3">Folders</h5>
          <ul className="list-group list-group-flush">
            <li className="list-group-item list-group-item-action">Inbox</li>
            <li className="list-group-item list-group-item-action">Sent</li>
            <li className="list-group-item list-group-item-action">Drafts</li>
            <li className="list-group-item list-group-item-action">Trash</li>
          </ul>
        </div>
        <div className="col-md-4 border-end">
          <h5 className="p-3">Email List</h5>
          <ul className="list-group list-group-flush">
            {sampleEmails.map((email) => (
              <li
                key={email.id}
                className="list-group-item list-group-item-action"
                onClick={() => setSelectedEmail(email)}
              >
                <div>
                  <strong>{email.sender}</strong> - {email.subject}
                </div>
                <small className="text-muted">{email.date}</small>
              </li>
            ))}
          </ul>
        </div>
        <div className="col-md-6">
          <h5 className="p-3">Email Viewer</h5>
          {selectedEmail ? (
            <div className="card">
              <div className="card-header">
                <div>
                  <strong>From:</strong> {selectedEmail.sender}
                </div>
                <div>
                  <strong>Subject:</strong> {selectedEmail.subject}
                </div>
                <div>
                  <small className="text-muted">{selectedEmail.date}</small>
                </div>
              </div>
              <div className="card-body">
                <p>{selectedEmail.body}</p>
              </div>
              <div className="card-footer">
                <button className="btn btn-primary">Reply</button>
                <button className="btn btn-danger ms-2">Delete</button>
              </div>
            </div>
          ) : (
            <p className="p-3">Select an email to view its content.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default EmailPage;
