const callAPI = async (kwargs) => {
  const { width, height, ...rest } = kwargs;
  const query = new URLSearchParams({
    ...rest,
    size: `${width}x${height}`,
  });
  const result = await fetch(`/?${query}`);
  return result.blob();
};

const h = (tag, attrs, ...children) => {
  const [nameWithId, ...rest] = tag.split(".");
  const [name, id] = nameWithId.split("#");
  const el = document.createElement(name || "div");
  if (id) {
    el.setAttribute("id", id);
  }
  el.className = rest.join(" ");
  const attrsIsChild =
    typeof attrs === "string" || attrs instanceof HTMLElement;
  if (attrs && !attrsIsChild) {
    Object.entries(attrs).forEach(([k, v]) => {
      if (v && typeof v === "object") {
        Object.assign(el[k], v);
      } else {
        el.setAttribute(k, v);
      }
    });
  }
  if (attrsIsChild) {
    el.append(attrs);
  }
  if (children.length) {
    el.append(...children);
  }
  return el;
};

const submit = async (kwargs, replaceAt) => {
  const image = h("img.w-full.show-in-modal.cursor-pointer", {
    src: URL.createObjectURL(await callAPI(kwargs)),
  });
  const container = h(".w-full.relative.mb-4", {}, image);
  container.addEventListener("mouseenter", (e) => {
    const regenerate = h(
      "px-2.py-2.bg-black.text-white.text-sm.absolute.cursor-pointer.bottom-0.right-0",
      "Retry",
    );
    regenerate.addEventListener("click", () => {
      regenerate.parentElement.removeChild(regenerate);
      submit(kwargs, container);
    });

    const onLeave = () => {
      container.removeEventListener("mouseleave", onLeave);
      regenerate.parentElement?.removeChild(regenerate);
    };
    container.addEventListener("mouseleave", onLeave);
    container.appendChild(regenerate);
  });

  image.addEventListener("click", (e) => {
    const dialog = h(
      "dialog",
      {
        style: {
          width: `${image.naturalWidth}px`,
          height: `${image.naturalHeight}px`,
        },
      },
      h("img", { src: e.target.src }),
    );
    document.body.appendChild(dialog);
    dialog.showModal();
    dialog.addEventListener("click", (e) => {
      dialog.close();
      dialog.parentElement?.removeChild(dialog);
    });
  });

  if (replaceAt) {
    replaceAt.replaceWith(container);
  } else {
    const output = document.querySelector("#output");
    output.insertBefore(container, output.firstChild);
  }
};

document.getElementById("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const kwargs = Object.fromEntries(new FormData(e.target));
  for (const prompt of kwargs.prompt.split("\n").filter((x) => x.trim())) {
    await submit({ ...kwargs, prompt });
  }
});

document.querySelector("textarea").addEventListener("keypress", async (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    const kwargs = Object.fromEntries(
      new FormData(document.getElementById("form")),
    );
    for (const prompt of kwargs.prompt.split("\n").filter((x) => x.trim())) {
      await submit({ ...kwargs, prompt });
    }
  }
});

document.querySelectorAll(".fill-size").forEach((el) =>
  el.addEventListener("click", (e) => {
    const size = e.target.innerText;
    const [width, height] = size.split("x");
    document.querySelector(`[name=width]`).setAttribute("value", width);
    document
      .querySelector(`[name=height]`)
      .setAttribute("value", height || width);
  }),
);
