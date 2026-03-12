#!/bin/bash

API_URL="http://localhost:8000/api/v1"
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "=== Todo API Test Script ==="
echo

echo "1. Health check"
response=$(curl -s "$API_URL/health")
echo "$response"
if echo "$response" | grep -q '"status":"ok"'; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
fi
echo

echo "2. Create tag 'Work'"
TAG_ID=$(curl -s -X POST "$API_URL/tags" \
  -H "Content-Type: application/json" \
  -d '{"name": "Work", "color": "#FF0000"}' | grep -o '"id":[0-9]*' | cut -d: -f2)
echo "Created tag with ID: $TAG_ID"
if [ -n "$TAG_ID" ]; then
    echo -e "${GREEN}✓ Tag created${NC}"
else
    echo -e "${RED}✗ Tag creation failed${NC}"
fi
echo

echo "3. Create tag 'Personal'"
TAG2_ID=$(curl -s -X POST "$API_URL/tags" \
  -H "Content-Type: application/json" \
  -d '{"name": "Personal", "color": "#00FF00"}' | grep -o '"id":[0-9]*' | cut -d: -f2)
echo "Created tag with ID: $TAG2_ID"
echo

echo "4. Get all tags"
curl -s "$API_URL/tags" | python3 -m json.tool
echo
echo -e "${GREEN}✓ Tags retrieved${NC}"
echo

echo "5. Create context 'Office'"
CTX_ID=$(curl -s -X POST "$API_URL/contexts" \
  -H "Content-Type: application/json" \
  -d '{"name": "Office", "description": "Work at office"}' | grep -o '"id":[0-9]*' | cut -d: -f2)
echo "Created context with ID: $CTX_ID"
if [ -n "$CTX_ID" ]; then
    echo -e "${GREEN}✓ Context created${NC}"
else
    echo -e "${RED}✗ Context creation failed${NC}"
fi
echo

echo "6. Create area 'Career'"
AREA_ID=$(curl -s -X POST "$API_URL/areas" \
  -H "Content-Type: application/json" \
  -d '{"name": "Career", "description": "Professional development"}' | grep -o '"id":[0-9]*' | cut -d: -f2)
echo "Created area with ID: $AREA_ID"
if [ -n "$AREA_ID" ]; then
    echo -e "${GREEN}✓ Area created${NC}"
else
    echo -e "${RED}✗ Area creation failed${NC}"
fi
echo

echo "7. Create project 'Learning'"
PROJ_ID=$(curl -s -X POST "$API_URL/projects" \
  -H "Content-Type: application/json" \
  -d '{"name": "Learning Python", "description": "Learn FastAPI", "area_id": "'"$AREA_ID"'"}' | grep -o '"id":[0-9]*' | cut -d: -f2)
echo "Created project with ID: $PROJ_ID"
if [ -n "$PROJ_ID" ]; then
    echo -e "${GREEN}✓ Project created${NC}"
else
    echo -e "${RED}✗ Project creation failed${NC}"
fi
echo

echo "8. Create task with tags"
TASK_ID=$(curl -s -X POST "$API_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete API tutorial", "description": "Finish the tutorial", "project_id": "'"$PROJ_ID"'", "context_id": "'"$CTX_ID"'", "tag_ids": ['"$TAG_ID"', '"$TAG2_ID"']}' | grep -o '"id":[0-9]*' | cut -d: -f2)
echo "Created task with ID: $TASK_ID"
if [ -n "$TASK_ID" ]; then
    echo -e "${GREEN}✓ Task created${NC}"
else
    echo -e "${RED}✗ Task creation failed${NC}"
fi
echo

echo "9. Get all tasks"
curl -s "$API_URL/tasks" | python3 -m json.tool
echo
echo -e "${GREEN}✓ Tasks retrieved${NC}"
echo

echo "10. Create inbox task"
INBOX_ID=$(curl -s -X POST "$API_URL/inbox" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, bread, eggs"}' | grep -o '"id":[0-9]*' | cut -d: -f2)
echo "Created inbox task with ID: $INBOX_ID"
if [ -n "$INBOX_ID" ]; then
    echo -e "${GREEN}✓ Inbox task created${NC}"
else
    echo -e "${RED}✗ Inbox task creation failed${NC}"
fi
echo

echo "11. Get inbox tasks"
curl -s "$API_URL/inbox" | python3 -m json.tool
echo
echo -e "${GREEN}✓ Inbox tasks retrieved${NC}"
echo

echo "12. Set task as next action"
if [ -n "$TASK_ID" ]; then
    curl -s -X POST "$API_URL/tasks/$TASK_ID/next-action" | python3 -m json.tool
    echo
    echo -e "${GREEN}✓ Task set as next action${NC}"
else
    echo -e "${RED}✗ Cannot set next action (no task ID)${NC}"
fi
echo

echo "13. Get next actions"
curl -s "$API_URL/tasks/next-actions" | python3 -m json.tool
echo
echo -e "${GREEN}✓ Next actions retrieved${NC}"
echo

echo "14. Complete task"
if [ -n "$TASK_ID" ]; then
    curl -s -X POST "$API_URL/tasks/$TASK_ID/complete" | python3 -m json.tool
    echo
    echo -e "${GREEN}✓ Task completed${NC}"
else
    echo -e "${RED}✗ Cannot complete task (no task ID)${NC}"
fi
echo

echo "15. Create subtask for project"
if [ -n "$PROJ_ID" ]; then
    curl -s -X POST "$API_URL/projects/$PROJ_ID/subtasks" \
      -H "Content-Type: application/json" \
      -d '{"title": "Read documentation", "task_id": "'"$TASK_ID"'"}' | python3 -m json.tool
    echo
    echo -e "${GREEN}✓ Subtask created${NC}"
else
    echo -e "${RED}✗ Cannot create subtask (no project ID)${NC}"
fi
echo

echo "16. Get project with subtasks"
if [ -n "$PROJ_ID" ]; then
    curl -s "$API_URL/projects/$PROJ_ID" | python3 -m json.tool
    echo
    echo -e "${GREEN}✓ Project with subtasks retrieved${NC}"
else
    echo -e "${RED}✗ Cannot get project (no project ID)${NC}"
fi
echo

echo "17. Get notifications"
curl -s "$API_URL/notifications" | python3 -m json.tool
echo
echo -e "${GREEN}✓ Notifications retrieved${NC}"
echo

echo "=== Test Script Complete ==="