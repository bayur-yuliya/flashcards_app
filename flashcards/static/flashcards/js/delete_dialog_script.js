function openDeleteDialog(id, name) {
  document.getElementById("deleteText").textContent = `Delete category ${name}?`;
  document.getElementById("deleteId").value = id;
  document.getElementById("deleteDialog").showModal();
}